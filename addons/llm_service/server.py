from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Modelo de datos para la entrada
class SensorData(BaseModel):
    sensor_id: str
    state: str
    room: str

@app.get("/")
def read_root():
    return {"message": "Complemento de Inferencia LLM."}

@app.post("/inferir")
async def inferir(data: SensorData):    
    print(f"Datos recibidos para inferencia: {data}")
    
    # LÓGICA DE INFERENCIA SIMULADA
    decision = "Ausente"
    if data.state == "on" and data.room == "Cocina":
        decision = "Presente"
    
    return {
        "presencia_inferida": decision,
        "habitación": data.room
    }