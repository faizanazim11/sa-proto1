from dotenv import load_dotenv

load_dotenv()

from scripts.config import Services

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=Services.HOST or "0.0.0.0", port=Services.PORT or 3001)
