from pipeline import document_analyzer


user_content = "RAG is a technique that combines information retrieval with text generation. It retrieves relevant documents from an external knowledge base and uses them as context when generating responses. This reduces hallucination because the model generates answers grounded in real retrieved facts rather than learned patterns alone."

user_level = "beginner" 
report1 =document_analyzer(user_content, user_level)

print(f'Report for Beginner:\n{report1}\n\n')

user_level = "expert"
report2 = document_analyzer(user_content, user_level)
print(f'Report for Expert:\n{report2}\n\n')