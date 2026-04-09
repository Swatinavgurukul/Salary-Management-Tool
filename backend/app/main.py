from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import employees, insights

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Salary Management API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees.router)
app.include_router(insights.router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}
