import os
import random
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# ==========================================
# 1. SERVIDOR WEB INTERNO (Mantiene el 24/7)
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "¡Bot en línea 24/7!"

def run():
    # Render asigna un puerto automáticamente, si no detecta la variable usa el 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ==========================================
# 2. CONFIGURACIÓN DEL BOT DE DISCORD
# ==========================================
intents = discord.Intents.default()
intents.message_content = True  # Obligatorio para leer el contenido de los mensajes

bot = commands.Bot(command_prefix="!", intents=intents)

# Lista de frases aleatorias
FRASES_TRABAJO = [
    '¿"Trabajo"? Prefiero llamarlo "mi próximo espectáculo de tiempo completo". Aunque si vas a ponerme a trabajar, asegúrate de que el presupuesto esté a la altura de mis pasos de baile.',
    '¿Ah, te refieres a lo que hago sobre el escenario o a limpiar monstruos en las Cavidades? Da igual, en ambos controlo el ritmo a la perfección. ¡Mantén los ojos abiertos si no quieres perderte el clímax!',
    'Si es por negocios, habla directamente. Pero si lo que quieres es que lidie con los caprichos de Sunna hoy... vas a tener que pagar el doble de comisiones.',
    '¡Por favor! No me vengas con esa cara de cansancio. El trabajo no es para llorar, es una oportunidad brillante para brillar... ¡y para asegurarnos de que la taquilla explote!',
    '¿Trabajar duro? El talento innato hace que todo parezca un juego de niños. Solo sígueme el paso y procura no arruinar mi combo perfecto.'
]

@bot.event
async def on_ready():
    print(f'Bot conectado con éxito como {bot.user}')

# Evento que escucha cada mensaje enviado en el servidor
@bot.event
async def on_message(message):
    # Evita que el bot se responda a sí mismo
    if message.author == bot.user:
        return

    # Comprueba si la palabra "trabajo" está en el mensaje (ignora mayúsculas/minúsculas)
    if "trabajo" in message.content.lower():
        frase_aleatoria = random.choice(FRASES_TRABAJO)
        await message.channel.send(frase_aleatoria)

    # Permite que otros comandos sigan funcionando si los añades en el futuro
    await bot.process_commands(message)

# ==========================================
# 3. ARRANQUE DEL SISTEMA
# ==========================================
if __name__ == "__main__":
    # Arranca el servidor web Flask en segundo plano
    keep_alive()
    
    # Inicia el bot leyendo el Token desde el entorno seguro de Render
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot.run(TOKEN)
