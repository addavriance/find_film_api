from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import router as search_router

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://192.168.1.86:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router, prefix="/api")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)