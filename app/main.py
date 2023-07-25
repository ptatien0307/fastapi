import psycopg2
from psycopg2.extras import RealDictCursor
import time
from fastapi import FastAPI


from .routers import post, user
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        connection = psycopg2.connect(host='localhost', database='fastapi',
                                      user='postgres', password='1597532684',
                                      cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print(f'Error: {error}')
        time.sleep(1)

app.include_router(user.router)