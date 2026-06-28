import httpx
import json
from http.server import BaseHTTPRequestHandler

FIREBASE_URL = "https://esp32aws-903f7-default-rtdb.firebaseio.com"
FIREBASE_SECRET = "5C88hVZ8RuJpAYQz6sXXrTkYY1B3wl4mT3JKaauU"

async def get_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{FIREBASE_URL}/sensores.json?auth={FIREBASE_SECRET}"
        )
        return response.json()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        import asyncio

        if self.path == "/api/latest":
            data = asyncio.run(get_data())
            readings = [v for v in data.values()
                       if isinstance(v, dict) and v.get('temperatura', 0) != 0]
            result = max(readings, key=lambda x: str(x.get('timestamp', ''))) if readings else {}

        elif self.path == "/api/all":
            data = asyncio.run(get_data())
            result = list(data.values()) if data else []

        elif self.path == "/api/summary":
            data = asyncio.run(get_data())
            readings = [v for v in data.values()
                       if isinstance(v, dict) and v.get('temperatura', 0) != 0]
            temps = [r['temperatura'] for r in readings]
            pres  = [r['presion'] for r in readings]
            result = {
                "total_lecturas": len(readings),
                "temperatura": { "min": min(temps), "max": max(temps), "promedio": round(sum(temps)/len(temps), 1) },
                "presion":     { "min": min(pres),  "max": max(pres),  "promedio": round(sum(pres)/len(pres), 1) }
            } if readings else {}
        else:
            result = {"error": "Endpoint no encontrado"}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())