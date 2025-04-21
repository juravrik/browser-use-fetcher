### 環境構築
```
uvx playwright install
```

### 動作確認
```
$uv run python src/server.py
$curl -X POST "http://localhost:8000/run" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "task": "このウェブサイトのタイトルを教えてください"
  }'
```