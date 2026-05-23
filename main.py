from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import tinytuya

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # W produkcji zamień "*" na adres swojej strony we Flasku, np. "https://twoja-strona.pl"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

DEVICE_ID = "bf900e4188fb9a2cd4wman"
DEVICE_IP = "192.168.226.149"
LOCAL_KEY = "dFDlt8$gQxg1eqHk"
VERSION = 3.5

def pobierz_dane_tuya():
    try:
        status = miernik.status()
        if "dps" in status:
            dps = status["dps"]
            return {
                "success": True,
                "napiecie": dps.get("20", dps.get("6", 0)) / 10.0,
                "prad": dps.get("18", dps.get("4", 0)) / 1000.0,
                "moc": dps.get("19", dps.get("5", 0)) / 10.0,
                "calkowite": dps.get("17", 0) / 100.0,
            }
        return {"success": False, "error": "Brak dps"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.websocket("/ws/power")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            dane = pobierz_dane_tuya()
            await websocket.send_json(dane)
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        pass

