import os
from openai import OpenAI

class AIService:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self.client = OpenAI(api_key=self.api_key)

    def generate_smart_reply(self, comment_text, prompt_template=None):
        """
        Generates a smart reply for a given comment.
        """
        if not prompt_template:
            prompt_template = f"You are an Instagram assistant. A user commented on a post with the following text: '{comment_text}'. Write a friendly and engaging reply."

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt_template},
                    {"role": "user", "content": comment_text}
                ],
                max_tokens=50,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating AI reply: {e}")
            return "Thank you for your comment!" # Fallback reply