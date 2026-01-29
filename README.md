# Реализация локального offline API RAG-бота с помощью Python

Модель эмбеддингов - all-MiniLM-L6-v2

LLM - Qwen3-0.6B (доступно без GPU)

Векторная база - Chroma

Демо доступно:
```sh 
docker compose up -d
```

Чтобы начать общение используйте curl или другой удобный инструмент:

Использование
> enable_thinking - думающий режим, добавляет "ход мысли"

> search_deep - глубина поиска, влияет на качество ответов, увеличивает время ответа
```sh 
curl -X POST http://127.0.0.1:5000/messages \
-H "Content-Type: application/json" \
-d '{"query": "Where Ynpen was born?", "enable_thinking": "true", "search_deep": "10"}'
```