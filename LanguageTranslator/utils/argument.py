import argparse


class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Translate English to Vietnamese.')
        self.parser.add_argument('--model_type', type=str, required=False, default='OpenAIModel',
                                 help='The type of translation model to use. Choose between "GLMModel" and "OpenAIModel".')
        self.parser.add_argument('--text', nargs='+', type=str, help='Input text(s) for translation.')
        self.parser.add_argument('--dest_language', type=str, help='Target language for translation.')
        self.parser.add_argument('--timeout', type=int, help='Timeout for the API request in seconds.')
        self.parser.add_argument('--openai_model', type=str, required=False,default='gpt-3.5-turbo',
                                 help='The model name of OpenAI Model. Required if model_type is "OpenAIModel".')
        self.parser.add_argument('--openai_api_key', type=str, required=False,default='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',
                                 help='The API key for OpenAIModel. Required if model_type is "OpenAIModel".')
        self.parser.add_argument('--json', type=str, help='Path to a JSON file for input')

    def parse_arguments(self):
        args = self.parser.parse_args()
        return args
