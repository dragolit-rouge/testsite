#fastapi код
import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Разрешение для гитхаба
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://smarthive.digital"], # Здесь будет адрес вашего сайта
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "smart_hive.db"

@app.get("/sensors")
def get_sensor_data():
    # Тот самый ваш код работы с SQLite файлом
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Пример запроса (замените на ваши таблицы)
    cursor.execute("SELECT * FROM telemetry ORDER BY id DESC LIMIT 20")
    rows = cursor.fetchall()
    
    conn.close()
    return {"status": "success", "data": rows}

@app.post("/add")
def add_data(temperature: float, humidity: float):
    # Сюда датчики будут бесплатно слать новые данные
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO telemetry (temperature, humidity) VALUES (?, ?)", 
        (temperature, humidity)
    )
    conn.commit()
    conn.close()
    
    # [ЗДЕСЬ БУДЕТ КОД]: Отправить обновленный файл .db в бесплатное облако, чтобы он не пропал
    
    return {"status": "saved"}
