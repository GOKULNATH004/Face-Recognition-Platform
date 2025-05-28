from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path
import sqlite3, os, cv2, base64
import numpy as np
from deepface import DeepFace

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

Path("registered_faces").mkdir(exist_ok=True)
os.makedirs("db", exist_ok=True)
DB_PATH = "db/registrations.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS faces (
            id TEXT,
            name TEXT,
            timestamp TEXT,
            image_path TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

class RegisterRequest(BaseModel):
    name: str
    id: str
    image: str

class RecognizeRequest(BaseModel):
    image: str

@app.post("/register")
def register(req: RegisterRequest):
    imgdata = base64.b64decode(req.image.split(",")[1])
    nparr = np.frombuffer(imgdata, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    folder = f"registered_faces/{req.name}_{req.id}"
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%B %d, %Y - %I:%M %p")
    filename = f"{folder}/{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    cv2.imwrite(filename, img)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO faces (id, name, timestamp, image_path) VALUES (?, ?, ?, ?)",
                (req.id, req.name, timestamp, filename))
    conn.commit()
    conn.close()

    return {"status": "success", "path": filename}

@app.post("/recognize")
def recognize(req: RecognizeRequest):
    imgdata = base64.b64decode(req.image.split(",")[1])
    nparr = np.frombuffer(imgdata, np.uint8)
    query_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    query_path = "temp_query.jpg"
    cv2.imwrite(query_path, query_img)

    try:
        results = DeepFace.find(img_path=query_path, db_path="registered_faces", enforce_detection=False)
        if results and not results[0].empty:
            matched_path = results[0].iloc[0]['identity']
            parts = matched_path.split(os.sep)[-2].split("_")
            matched_name = parts[0]
            matched_id = parts[1]

            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT timestamp FROM faces WHERE name=? AND id=? ORDER BY timestamp DESC LIMIT 1", (matched_name, matched_id))
            db_row = cur.fetchone()
            conn.close()

            return {
                "results": [{
                    "name": matched_name,
                    "id": matched_id,
                    "timestamp": db_row[0] if db_row else "N/A"
                }]
            }
        else:
            return {"results": []}
    except Exception as e:
        return {"error": str(e)}
    
class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def chat(req: ChatRequest):
    q = req.question.lower()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if "last" in q and "register" in q:
        cur.execute("SELECT name, id, timestamp FROM faces ORDER BY timestamp DESC LIMIT 1")
        row = cur.fetchone()
        conn.close()
        if row:
            return {"answer": f"{row[0]} (ID: {row[1]}) registered at {row[2]}."}
        return {"answer": "No registrations found."}

    elif "id of" in q:
        name = q.split("id of")[-1].strip()
        cur.execute("SELECT id FROM faces WHERE name LIKE ? ORDER BY timestamp DESC LIMIT 1", (f"%{name}%",))
        row = cur.fetchone()
        conn.close()
        if row:
            return {"answer": f"The ID of {name.title()} is {row[0]}."}
        return {"answer": f"No user found with name {name}."}

    elif "when did" in q and "register" in q:
        name = q.split("when did")[-1].split("register")[0].strip()
        cur.execute("SELECT timestamp FROM faces WHERE name LIKE ? ORDER BY timestamp DESC LIMIT 1", (f"%{name}%",))
        row = cur.fetchone()
        conn.close()
        if row:
            return {"answer": f"{name.title()} registered on {row[0]}."}
        return {"answer": f"No registration found for {name}."}

    conn.close()
    return {"answer": "I can help with registration info. Try asking: 'Who registered last?' or 'What is the ID of Harini?'"}