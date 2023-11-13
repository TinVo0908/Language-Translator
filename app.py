import gradio as gr
from translator import ServerTranslator
import json


def clear_all(input_json, input_text, input_dest_lang, translated_text):
    return None, "", "", ""


def translate_text_json(input_json):
    # Translation code for JSON input
    try:
        json_file_path = input_json.name
        with open(json_file_path, 'r') as f:
            file_content = f.read()
            json_input = json.loads(file_content)
            translation = ServerTranslator.language_translator(inputs_data=json_input).translate()
            translate_text = translation['text']
        return translate_text
    except Exception as e:
        translate_text = f"Error: {str(e)}"


def translate_text_text(input_text, input_dest_lang):
    # Translation code for text input
    try:
        translation = ServerTranslator.language_translator(text=input_text, dest_language=input_dest_lang).translate()
        translate_text = translation['text']
        return translate_text
    except Exception as e:
        translate_text = f"Error: {str(e)}"


with gr.Blocks() as demo:
    input_json = gr.components.File(label="Upload JSON file")
    input_dest_lang = gr.components.Textbox(placeholder='Example input: vi',label="Destination Language")
    input_text = gr.components.Textbox(placeholder='Example inputs: I love you, I love you than myself', label="Enter Text")
    translated_text = gr.components.Textbox(placeholder='Example outputs: Anh yêu em, Anh yêu em hơn bản thân mình',
                                            label="Translated Text")

    with gr.Column():
        submit_json = gr.Button("Submit Json")
        submit_text = gr.Button("Submit Text")
        submit_json.click(
            translate_text_json,
            [input_json],  # Pass all three inputs
            [translated_text]
        )
        with gr.Column():
            submit_text.click(
                translate_text_text,
                [input_text, input_dest_lang],  # Pass all three inputs
                [translated_text]
            )
        clear = gr.Button("Clear")
        clear.click(
            clear_all,
            [input_json, input_text, input_dest_lang, translated_text],
            [input_json, input_text, input_dest_lang, translated_text]
        )

demo.launch(share=True)
