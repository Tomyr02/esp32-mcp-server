import httpx
from fastmcp import FastMCP

FIREBASE_URL = "https://esp32aws-903f7-default-rtdb.firebaseio.com"
FIREBASE_SECRET = "tu-firebase-secret"

mcp = FastMCP(
    "ESP32 Sensor Server",
    auth=None  # Sin autenticación
)

@mcp.tool()
async def get_latest_reading() -> dict:
    """Obtiene la última lectura del sensor ESP32 (temperatura y presión)"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{FIREBASE_URL}/sensores.json?auth={FIREBASE_SECRET}"
        )
        data = response.json()
        if data and isinstance(data, dict):
            readings = [v for v in data.values() 
                       if isinstance(v, dict) and v.get('temperatura', 0) != 0]
            if readings:
                latest = max(readings, key=lambda x: x.get('timestamp', 0))
                return latest
        return {"error": "No data found"}

@mcp.tool()
async def get_latest_temp_pressure() -> dict:
    """Obtiene la última temperatura y presión del sensor ESP32"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{FIREBASE_URL}/sensores.json?auth={FIREBASE_SECRET}"
        )
        data = response.json()
        if not data:
            return {"error": "No data found"}

        last_key = list(data.keys())[-1]
        last = data[last_key]
        return {
            "timestamp": last_key,
            "temperatura": last.get("temperatura"),
            "presion": last.get("presion"),
        }

@mcp.tool()
async def get_all_readings() -> dict:
    """Obtiene todas las lecturas del sensor ESP32"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{FIREBASE_URL}/sensores.json?auth={FIREBASE_SECRET}"
        )
        return response.json()

@mcp.tool()
async def get_readings_summary() -> dict:
    """Obtiene un resumen estadístico de las lecturas del sensor"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{FIREBASE_URL}/sensores.json?auth={FIREBASE_SECRET}"
        )
        data = response.json()
        if not data:
            return {"error": "No data found"}

        readings = list(data.values())
        temperaturas = [r['temperatura'] for r in readings if 'temperatura' in r]
        presiones = [r['presion'] for r in readings if 'presion' in r]

        return {
            "total_lecturas": len(readings),
            "temperatura": {
                "min": min(temperaturas),
                "max": max(temperaturas),
                "promedio": round(sum(temperaturas) / len(temperaturas), 1)
            },
            "presion": {
                "min": min(presiones),
                "max": max(presiones),
                "promedio": round(sum(presiones) / len(presiones), 1)
            }
        }

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)