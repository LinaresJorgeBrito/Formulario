from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def init_db():
    with sqlite3.connect("form_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS form_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                apellido TEXT,
                matricula REAL,
                asignatura REAL,
                profesor TEXT,
                edad REAL
            )
        """)
        conn.commit()

@app.on_event("startup")
async def startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def process_form(request: Request, nombre: str = Form(...), apellido: str = Form(...), matricula: int = Form(...), asignatura: str = Form(...), profesor: str = Form(...), edad: int = Form(...)):
    with sqlite3.connect("form_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO form_data (nombre, apellido, matricula, asignatura, profesor, edad) VALUES (?, ?, ?, ?,?,?)",
                       (nombre, apellido, matricula, asignatura, profesor, edad))
        conn.commit()
    return templates.TemplateResponse("data.html", {"request": request, "data": {"nombre": nombre, "apellido": apellido, "matricula": matricula, "asignatura": asignatura, "profesor": profesor, "edad": edad}})

@app.get("/records", response_class=HTMLResponse)
async def get_records(request: Request):
    with sqlite3.connect("form_data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, apellido, matricula, asignatura, profesor, edad FROM form_data")
        records = cursor.fetchall()
    return templates.TemplateResponse("records.html", {"request": request, "records": records})
