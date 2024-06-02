from fastapi import FastAPI
from src.api import router as search_router

app = FastAPI()

app.include_router(search_router, prefix="/api")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
