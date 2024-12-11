from fastapi import FastAPI, Response, status, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import time
from api.v1 import main


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",

]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    log_message = f"{request.method} {request.url} completed in {process_time:.4f} secs"
    print(log_message)
    return response
app.include_router(main.router, prefix='/api/v1')