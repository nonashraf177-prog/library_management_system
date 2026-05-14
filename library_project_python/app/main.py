#main

from fastapi import FastAPI
from app.core.database import engine, Base
from app.models import user_model, book_model, borrow_model 
from app.routes import auth_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System")

app.include_router(auth_routes.router)

@app.get("/")
def read_root():
    return {"status": "Project is running!"}