import fastapi
import sqlite3
import uvicorn
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class fbModel(BaseModel):
    email: str
    msg: str
    subject: str

class DataBase:
    def __init__(self):
        self.connect = sqlite3.connect('db.sqlite3')
        self.cursor = self.connect.cursor()

    def create_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS feedback (
            email VARCHAR(100),
            msg VARCHAR(500),
            subject VARCHAR(100)
        )
        """
        self.cursor.execute(sql)
        self.connect.commit()

    def new_feedback(self, email, msg, subject):
        sql = f"INSERT INTO feedback VALUES ('{email}', '{msg}', '{subject}')"
        self.cursor.execute(sql)
        self.connect.commit()

    def get_fb(self):
        return self.cursor.execute("SELECT * FROM feedback").fetchall()


@app.post('/feedback')
def feedback(data:fbModel|dict):
    db = DataBase()
    db.create_table()
    feedback = db.new_feedback(email=data.email, msg=data.msg, subject=data.subject)
    return True

@app.get('/feedback')
def get():
    db = DataBase()
    db.create_table()
    fb = db.get_fb()
    return str(fb)

if __name__ == '__main__':
    uvicorn.run('app:app', host='127.0.0.1', port = 5000, reload=True)