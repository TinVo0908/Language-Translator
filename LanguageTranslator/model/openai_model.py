import openai
import time
import math

class Model:
    def make_text_prompt(self, text: str, target_language: str) -> str:
        # Create a text prompt for translation
        return f"Translate to {target_language}: {text}"

    def translate_prompt(self, content, target_language: str) -> str:
        # Generate a translation prompt based on the content type
        if isinstance(content, (str, list)):
            return self.make_text_prompt(content, target_language)

    def make_request(self, prompt):
        # Subclasses must implement this method to send the request
        raise NotImplementedError("Subclasses must implement the make_request method")


class OpenAIModel(Model):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        openai.api_key = api_key

    def make_translation_request(self, prompt):
        attempts = 0
        while attempts < 3:
            try:
                if self.model_name == "gpt-3.5-turbo":
                    response = openai.ChatCompletion.create(
                        model=self.model_name,
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )
                    translation = response.choices[0].message['content'].strip()
                else:
                    response = openai.ChatCompletion.create(
                        model=self.model_name,
                        prompt=prompt,
                        max_tokens=150,
                        temperature=0
                    )
                    translation = response.choices[0].text.strip()

                return translation, True
            except openai.error.RateLimitError:
                attempts += 1
                if attempts < 3:
                    wait_time = math.pow(2, attempts)  # exponential backoff
                    print("Rate limit reached. Waiting for 60 seconds before retrying.")
                    time.sleep(60)
                else:
                    raise Exception("Rate limit reached. Maximum attempts exceeded.")
        return "", False
