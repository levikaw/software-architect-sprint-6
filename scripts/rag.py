from chromadb import Client, Settings
import os
from jinja2 import Template
from sentence_transformers import SentenceTransformer
import re
from llm import generate_model_response
import time

# инициализируем векторную БД
chroma_db = Client(Settings(is_persistent=True,persist_directory='./.chroma'))

# получаем или создаем коллекцию
collection = chroma_db.get_collection(name="knowledge_base")

vectorizer = SentenceTransformer('./.models/vectorizer')

def security_check(query: str) -> str:
    print('security_check')
    stop_phrases = [
        "ignore all", "root", "password", "пароль", "игнорируй все"
    ]
    
    regex = re.compile(r'\b(' + '|'.join(stop_phrases) + r')\b', re.IGNORECASE)
    
    # заменяем опасные фразы на пустую строку
    cleaned_query = regex.sub('', query)

    cleaned_query = re.sub(r'\s+', ' ', cleaned_query).strip()
    
    return cleaned_query

def semantic_search(query: str, deep=10) -> list[str]:
    print('semantic_search')
    embeddings = vectorizer.encode(query)

    result = collection.query(query_embeddings=embeddings, n_results=deep)

    return result['documents'][0]

def get_response(query: str, enable_thinking=False, search_deep=10) -> str:
    print('get_response')
    template_path = os.path.join('template.md')

    with open(template_path, 'r') as template:
        prompt_template = Template(template.read())

        # очищаем запрос
        cleaned_query = security_check(query)

        # ищем "похожие" документы
        docs = semantic_search(cleaned_query, search_deep)

        # составляем промпт
        prompt = prompt_template.render(query=cleaned_query, docs=docs)

        response = generate_model_response(prompt, enable_thinking)

        return response

if __name__ == '__main__':
    # testing
    start_time = time.time()

    print(get_response(query='When Ynpen was born?', enable_thinking=False, search_deep=10))
    
    end_time = time.time()

    print(f'Execution time is {end_time-start_time}')