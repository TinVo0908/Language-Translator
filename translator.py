import json
import time
from LanguageTranslator.utils.argument import ArgumentParser
from LanguageTranslator.model.openai_model import OpenAIModel
from fastapi import HTTPException


class LocalTranslator:
    def __init__(self, open_ai, inputs_data):
        # Initialize the LocalTranslator with OpenAI and inputs data
        self.open_ai = open_ai
        self.inputs_data = inputs_data

    def translate(self):
        # Translates the provided text into the destination language
        translations = []
        result_response = {
            'text': '',
            'language_translation': ''
        }

        if 'text' not in self.inputs_data or 'dest_language' not in self.inputs_data:
            print("Required fields 'text' and 'dest_language' are missing in input data.")
            return translations, ''

        text = self.inputs_data['text']
        dest_language = self.inputs_data['dest_language']

        if not isinstance(dest_language, str):
            print("Destination language is not a single text.")
            return translations, dest_language

        if isinstance(text, str):
            text = [text]

        if not isinstance(text, list):
            print("Input data is not a text or a list of text")
            return translations, dest_language

        start_time = time.time()
        for t in text:
            prompt = self.open_ai.translate_prompt(t, dest_language)
            translation, _ = self.open_ai.make_translation_request(prompt)
            translations.append(translation)
        end_time = time.time()

        execution_time = end_time - start_time
        result_response['text'] = translations if len(translations) > 1 else translations[0]
        result_response['language_translation'] = dest_language
        print(f"Translation completed in {execution_time:.2f} seconds 🎉🎉🎉\nTranslated: {result_response}")
        return result_response

    @classmethod
    def load_parser(cls):
        # Loads the parser object for argument parsing
        argument_parser = ArgumentParser()
        args = argument_parser.parse_arguments()
        return args

    @classmethod
    def language_translator(cls):
        # Builds the language translator using the provided arguments
        args = cls.load_parser()
        if args.model_type == "OpenAIModel":
            if args.openai_model and args.openai_api_key:
                model_name = args.openai_model
                api_key = args.openai_api_key
            else:
                raise ValueError("Invalid OpenAI model or API key")
            model = OpenAIModel(model_name=model_name, api_key=api_key)
        else:
            raise ValueError("Invalid OpenAIModel specified.")

        if args.json:
            with open(args.json, 'r') as j:
                input_data = json.load(j)
        else:
            input_data = {
                "text": args.text,
                "dest_language": args.dest_language
            }

        return cls(open_ai=model, inputs_data=input_data)


class ServerTranslator:
    def __init__(self, open_ai, inputs_data):
        # Initialize the ServerTranslator with OpenAI and inputs data
        self.open_ai = open_ai
        self.inputs_data = inputs_data

    def translate(self):
        # Translates the given text into the destination language
        translations = []
        result_response = {
            'text': '',
            'language_translation': ''
        }

        if 'text' not in self.inputs_data or 'dest_language' not in self.inputs_data:
            raise HTTPException(status_code=400,
                                detail="Required fields 'text' and 'dest_language' are missing in input data.")

        text = self.inputs_data['text']
        dest_language = self.inputs_data['dest_language']

        if not isinstance(dest_language, str):
            raise HTTPException(status_code=400, detail="Destination language is not a single text.")

        if isinstance(text, str):
            text = text.split(',')
            text = [text]

        if not isinstance(text, list):
            raise HTTPException(status_code=400, detail="Input data is not a text or a list of text.")

        start_time = time.time()
        for t in text:
            prompt = self.open_ai.translate_prompt(t, dest_language)
            translation, _ = self.open_ai.make_translation_request(prompt)
            translations.append(translation)
        end_time = time.time()
        execution_time = end_time - start_time
        result_response['text'] = translations if len(translations) > 1 else translations[0]
        result_response['language_translation'] = dest_language
        print(f"Translation completed in {execution_time:.2f} seconds 🎉🎉🎉\nTranslated: {result_response}")
        return result_response

    @classmethod
    def language_translator(cls, inputs_data=None, text=None, dest_language=None,
                            model_type='OpenAIModel', openai_model='gpt-3.5-turbo',
                            openai_api_key='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'):
        # Builds the language translator using the provided arguments
        if model_type == "OpenAIModel":
            if openai_model and openai_api_key:
                model_name = openai_model
                api_key = openai_api_key
            else:
                raise HTTPException(status_code=400, detail="Invalid OpenAI model or API key")
            model = OpenAIModel(model_name=model_name, api_key=api_key)
        else:
            raise HTTPException(status_code=400, detail="Invalid OpenAIModel specified.")

        if inputs_data:
            input_data = {
                "text": inputs_data['text'].split(','),
                "dest_language": inputs_data['dest_language']
            }
        else:
            input_data = {
                "text": text,
                "dest_language": dest_language
            }
        return cls(open_ai=model, inputs_data=input_data)


# if __name__ == "__main__":
#     process = LocalTranslator.language_translator()
#     process.translate()
