from fastapi import FastAPI
from .routers import auth, categories, transactions, statistics
from .database import Base, engine
from fastapi.middleware.cors import CORSMiddleware


# DB 테이블 생성
Base.metadata.create_all(bind=engine)



app = FastAPI(title="가계부 API (MySQL)")

origins = [
    "http://localhost:3000",  # 웹에서 테스트할 경우
    "http://127.0.0.1:3000",
    "http://10.0.2.2:3000",   # Android 에뮬레이터
    "http://10.0.2.2:8081",   # React Native Metro Bundler (Android)
    "http://localhost:8081",  # iOS 시뮬레이터
    "*"                       # 개발 단계에서는 전체 허용 가능
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # 허용할 origin 리스트
    allow_credentials=True,
    allow_methods=["*"],            # 모든 HTTP 메서드 허용 (GET, POST 등)
    allow_headers=["*"],            # 모든 헤더 허용
)


app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(statistics.router)