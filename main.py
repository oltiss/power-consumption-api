from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import tinytuya, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # W produkcji zamień "*" na adres swojej strony we Flasku, np. "https://twoja-strona.pl"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

DEVICE_ID = os.getenv("DEVICE_ID")
DEVICE_IP = os.getenv("DEVICE_IP")
LOCAL_KEY = os.getenv("LOCAL_KEY")
VERSION = float(os.getenv("VERSION"))


miernik = tinytuya.OutletDevice(DEVICE_ID, DEVICE_IP, LOCAL_KEY)
miernik.set_version(VERSION)
status = miernik.status()

def pobierz_dane_tuya():
    try:
        status = miernik.status()
        if "dps" in status:
            dps = status["dps"]
            return {
                "success": True,
                "napiecie": dps.get("20", dps.get("6", 0)) / 10.0,
                "prad": round(dps.get("18", dps.get("4", 0)) / 1000.0, 2),
                "moc": dps.get("19", dps.get("5", 0)) / 10.0,
                "zuzycie": dps.get("17", 0) / 100.0,
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


@app.get('/pwr')
def get_data():
    dane = pobierz_dane_tuya()
    return dane
