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

        # Step 2 →  Extract the key entities and concepts from the text
        system_instruction = f"""You are a senior software engineer with 20 years of experience in different domains most of the time in AI engineering. You have to extract the 5 key concepts, you have summarized user content {summary} and the original content is {user_content}. You have to extract the key concepts and entities from the user content. You have to return the output in a list format. final output should be in this: 
        {{
            'key_concepts': [
                {{
                    'concept': 'concept1',
                    'description': 'what and why it is important in 30 words'
                }},
                ...
            ],
            'complexity': 'concept complexity - normal, intermediate, complex'
        }}
        
        description should be in 30 words, complexity depends on how complex the concept of key concept is.
        """

        key_concepts = run_llm(user_content, system_instruction)
        # Robustly parse JSON from model output: strip markdown fences and extract JSON substring
        def _extract_json(s: str) -> str:
            if not s or not s.strip():
                return s
            text = s.strip()
            # remove triple-backtick fences
            if text.startswith('```') and text.endswith('```'):
                # drop the first/last fence lines
                parts = text.split('\n')
                # if fence includes language, remove first line
                parts = parts[1:-1]
                text = '\n'.join(parts).strip()
            # If the model included a markdown JSON block like ```json ... ``` handle above
            # Try to find a JSON object inside the text by locating outermost braces
            first = text.find('{')
            last = text.rfind('}')
            if first != -1 and last != -1 and last > first:
                return text[first:last+1]
            return text

        raw = key_concepts.get('text') if isinstance(key_concepts, dict) else key_concepts
        cleaned = _extract_json(raw)
        try:
            key_concepts_obj = json.loads(cleaned)
        except Exception:
            print('Failed to parse key_concepts JSON. Raw output:')
            print(raw)
            raise
        input_tokens += key_concepts['input_tokens']
        output_tokens += key_concepts['output_tokens']
        report['key_concepts'] = key_concepts_obj
        # Step 3  →  Generate 3 Q&A pairs that test understanding — return as JSON
        system_instruction = f"""You are a senior software engineer mentor with 20 years of experience in different domains most of the time in AI engineering. You have to generate 3 Q&A pairs that test understanding of the user content. user content is {user_content} and the summary is {summary} and key concepts are {key_concepts}. You have to return the output in a JSON format. final output should be in this: 
        {{
            'qna_pairs': [
                {{
                    'question': 'question1',
                    'answer': 'answer of question1'
                }},
                ...
            ]
        }}
        """

        qna_pairs = run_llm(user_content, system_instruction)
        raw_qna = qna_pairs.get('text') if isinstance(qna_pairs, dict) else qna_pairs
        cleaned_qna = _extract_json(raw_qna)
        try:
            qna_pairs_obj = json.loads(cleaned_qna)
        except Exception:
            print('Failed to parse qna_pairs JSON. Raw output:')
            print(raw_qna)
            raise
        input_tokens += qna_pairs['input_tokens']
        output_tokens += qna_pairs['output_tokens']
        report['qna_pairs'] = qna_pairs_obj
        
        return report

    except Exception as e:
        print(f"Error: {e}")
        raise e

