from dotenv import load_dotenv

load_dotenv()

from scripts.config import Services
from scripts.core.schemas.pg_models import create_db_and_tables

if __name__ == "__main__":
    create_db_and_tables()
    import uvicorn

    uvicorn.run("main:app", host=Services.HOST or "0.0.0.0", port=Services.PORT or 3001)
