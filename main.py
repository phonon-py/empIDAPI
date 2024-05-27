from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class Name(BaseModel):
    name: str

def init_db():
    conn = sqlite3.connect('names.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS names
                      (id INTEGER PRIMARY KEY, name TEXT)''')
    conn.commit()
    conn.close()

@app.post("/submit")
async def submit_name(name: Name):
    conn = sqlite3.connect('names.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO names (name) VALUES (?)", (name.name,))
    conn.commit()
    conn.close()
    return {"message": "Name inserted successfully"}

@app.get("/names")
async def get_names():
    conn = sqlite3.connect('names.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM names")
    names = [{"name": row[0]} for row in cursor.fetchall()]
    conn.close()
    return names

init_db()