# Profit Test Task

Мини-сервис уведомлений на FastAPI с поддержкой WebSocket.

## Запуск

### Через Docker

1. Собрать образ:
```bash
docker build -t profit-test-task .
```

2. Запустить контейнер:
```bash
docker run -p 8000:8000 profit-test-task
```

Сервис будет доступен по адресу: `http://localhost:8000`

---

### Локально

1. Создать виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Установить зависимости:
```bash
pip install -r requirements.txt
```

3. Запустить сервис:
```bash
uvicorn app.main:app --reload
```

---

## API

### POST /events

Принимает событие о задаче.

```bash
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "type": "job.started",
    "product": "my_product",
    "job_id": "123",
    "timestamp": "2026-03-13T10:01:00Z",
    "payload": {
      "status": "started"
    }
  }'
```

---

### WS /ws

Подписка на обновления задачи.

1. Подключиться к `ws://localhost:8000/ws`
2. Отправить сообщение для подписки:
```json
{
  "action": "subscribe",
  "job_id": "123"
}
```
3. Если задача уже существует — сервер сразу вернёт последнее состояние
4. При каждом новом событии — сервер отправит обновление
