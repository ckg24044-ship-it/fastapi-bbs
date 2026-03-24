from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.routers import threads
from app.routers import posts
from app.database import get_db

app = FastAPI(
    title="BBS API",
    description="Simple Bulletin Board System API",
    version="0.1"
)

# ルーター
app.include_router(threads.router)
app.include_router(posts.router)
app.include_router(posts.threads_router)

# 静的ファイル
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# テンプレート
templates = Jinja2Templates(directory="app/templates")

# ==========================
# トップページ（ここ重要🔥）
# ==========================
@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):

    threads_data = db.execute(
        text("SELECT * FROM threads ORDER BY created_at DESC")
    ).fetchall()

    latest_posts = db.execute(
        text("SELECT * FROM posts ORDER BY created_at DESC LIMIT 10")
    ).fetchall()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "threads": threads_data,
        "latest_posts": latest_posts
    })

    # スレッド一覧
    threads_data = db.execute(
        "SELECT * FROM threads ORDER BY created_at DESC"
    ).fetchall()

    # 最新投稿10件
    latest_posts = db.execute(
        "SELECT * FROM posts ORDER BY created_at DESC LIMIT 10"
    ).fetchall()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "threads": threads_data,
        "latest_posts": latest_posts
    })