from fastapi import FastAPI
from app.api import routes

app = FastAPI()

# include your routes
app.include_router(routes.router)
