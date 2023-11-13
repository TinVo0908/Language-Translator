# Language Translator 
## Introduction 
Open AI Translator is the Power tool to translate English to Vietnamese Language. Using the Large Language Model (LLM) like GPT-3.5-turbo, ... for translation

The project is built in Python Which include API by FastAPI and User Interface by Gradio 

## Getting Started
### Environment Setup
1. Clone the repository: 
   ```commandline
   git clone git@github.com:TinVo0908/Language-Translator.git'
   ```
2. The project is require: Python 3.9+ 
3. Install dependencies by:
    ```
   pip install -r requirements.txt
   ```
### How to Use 
1. For running with command line in terminal: 
   For input is text and dest_language 
    ```commandline
    python test_local_translator.py --text 'your input text' --dest_language 'vi'
    ```
   For input is json file 
    ```commandline
    python test_local_translator.py --json 'your json file' 
    ```
   Noted: You can set your api key with argument --openai_api_key and set the model name with --openai_model or you can use api key and model with my default.
2. For running API: 
   ```commandline
   uvicorn api:app --reload
   ```
3. For running User Interface
   ```commandline
   python app.py 
   ```
