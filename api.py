from fastapi import FastAPI, UploadFile, Query, HTTPException
from starlette.responses import RedirectResponse
from typing import Union, List
from pydantic import BaseModel
from translator import ServerTranslator
import json
import uvicorn

app = FastAPI()


# Define a data model for the input
class TranslationInput(BaseModel):
    text: str
    dest_language: str


class TranslationResult(BaseModel):
    text: Union[str, List[str]]
    language_translation: str


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")


@app.post("/translate", response_model=TranslationResult)
async def run_translation_manual(
        text: str = Query(..., description="Input text to translate"),
        dest_language: str = Query(..., description="Destination language")):
    # Splitting the input text
    text = text.split(',')
    # Creating and processing the translator
    processing_language = ServerTranslator.language_translator(
        text=text,
        dest_language=dest_language,
    )
    # Getting the translated result
    result_response = processing_language.translate()
    return result_response


@app.post("/translate_json", response_model=TranslationResult)
async def run_translation_auto(json_file: UploadFile):
    try:
        # Reading the JSON content from the file
        json_content = await json_file.read()
        json_data = json.loads(json_content.decode("utf-8"))
        # Creating and processing the translator
        processing_language = ServerTranslator.language_translator(
            json_data
        )
        # Getting the translated result
        result_response = processing_language.translate()
        return result_response
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON input")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
