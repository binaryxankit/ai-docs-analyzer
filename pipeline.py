from utils import run_llm, input_sanitizer_check, cost_calculator
import json

def document_analyzer(user_content, user_level):
    try:

        report = {}
        input_tokens = 0
        output_tokens = 0
        sanitizer = input_sanitizer_check(user_content)
        if not sanitizer:
            print("Input content failed sanitization check. Potential prompt injection detected.")
            return
        
        # Step 1  →  Summarize the text in under 100 words
        system_instruction = f"You are technical writer that have 20 years of experience writing technical content and summarize the complex technical concepts for the engineering teams. You must summarize the content in under 100 words. You know which word is necessary or needed in summary so that actual meaning of the content will not be lost."
        summary = run_llm(user_content, system_instruction)
        input_tokens += summary['input_tokens']
        output_tokens += summary['output_tokens']
        report['summary'] = summary['text']

        return report

    except Exception as e:
        print(f"Error: {e}")
        raise e

