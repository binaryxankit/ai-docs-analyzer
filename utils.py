from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GENAI_API_KEY")
model_name = os.getenv("MODEL")

def run_llm(user_content:str, system:str):
    # Create a GenAI client

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=model_name,
            contents=user_content,
            config={
                "temperature": 0,
                "system_instruction": system
            }
        )
        return {
            "text": response.text,
            "input_tokens": response.usage_metadata.prompt_token_count,
            "output_tokens": response.usage_metadata.candidates_token_count
        }
    except Exception as e:
        print(f"Error: {e}")
        raise e
    