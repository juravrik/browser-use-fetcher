import os
from fastapi import FastAPI
from pydantic import BaseModel, SecretStr
from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# APIキーの設定
load_dotenv()
api_key_deepseek = os.getenv('DEEPSEEK_API_KEY', '')
if not api_key_deepseek:
	raise ValueError('DEEPSEEK_API_KEY is not set')

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

# リクエストボディのモデルを定義
class TaskRequest(BaseModel):
    url: str
    task: str

# browser-useを実行するエンドポイントを定義
@app.post("/run")
async def run_browser_task(request: TaskRequest):
    """
    指定されたURLとタスクでbrowser-useエージェントを実行します。
    """
    browser = Browser(
	    config=BrowserConfig(
		    headless=True,
		    disable_security=True,
	)
)
    llm = ChatOpenAI(
		base_url='https://api.deepseek.com/v1',
		model='deepseek-chat',
		api_key=SecretStr(api_key_deepseek),
	)
    agent = Agent(task=request.task, llm=llm, use_vision=False, browser=browser)
    result = await agent.run()
    return result
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)