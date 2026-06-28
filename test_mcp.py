import asyncio
from server import mcp  # Importamos la instancia de tu servidor

async def probar_servidor():
    print("🔍 Iniciando prueba local del servidor MCP...")
    try:
        # Agregamos 'await' porque list_tools() es una corrutina
        herramientas = await mcp.list_tools()
        
        # Buscamos la que necesitamos
        nombre_herramienta = "get_latest_temp_pressure"
        herramienta_encontrada = next((t for t in herramientas if t.name == nombre_herramienta), None)
        
        if not herramienta_encontrada:
            print(f"❌ Error: No se encontró la herramienta '{nombre_herramienta}' en server.py")
            print(f"Herramientas disponibles: {[t.name for t in herramientas]}")
            return

        print("📡 Llamando a la función y conectando con Firebase...")
        
        # Ejecutamos la herramienta de forma asíncrona
        resultado = await mcp.call_tool(nombre_herramienta, arguments={})
        
        print("\n✅ ¡Conexión exitosa! Respuesta recibida de Firebase:")
        print("-" * 50)
        print(resultado)
        print("-" * 50)

    except Exception as e:
        print(f"\n❌ Ocurrió un error al ejecutar la prueba: {e}")

# Arrancar la prueba
asyncio.run(probar_servidor())