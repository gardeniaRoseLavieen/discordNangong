import os
import random
import re  # Importamos Expresiones Regulares para limpiar el texto
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

# Lista completa de frases aleatorias (las originales + las nuevas de Idol/Cavidades)
FRASES_TRABAJO = [
    '¿"Trabajo"? Prefiero llamarlo "mi próximo espectáculo de tiempo completo". Aunque si vas a ponerme a trabajar, asegúrate de que el presupuesto esté a la altura de mis pasos de baile.',
    '¿Ah, te refieres a lo que hago sobre el escenario o a limpiar monstruos en las Cavidades? Da igual, en ambos controlo el ritmo a la perfección. ¡Mantén los ojos abiertos si no quieres perderte el clímax!',
    'Si es por negocios, habla directamente. Pero si lo que quieres es que lidie con los caprichos de Sunna hoy... vas a tener que pagar el doble de comisiones.',
    '¡Por favor! No me vengas con esa cara de cansancio. El trabajo no es para llorar, es una oportunidad brillante para brillar... ¡y para asegurarnos de que la taquilla explote!',
    '¿Trabajar duro? El talento innato hace que todo parezca un juego de niños. Solo sígueme el paso y procura no arruinar mi combo perfecto.',
    '¿Trabajo? Mientras las cámaras apunten hacia mí y las comisiones lleguen a tiempo, no me importa si tengo que bailar en un concierto o patear etéreos en una Cavidad.',
    '¿Que si estoy cansada? ¡Ja! Un genio no conoce el agotamiento. El único "trabajo" real aquí es lograr que tú no te quedes atrás mirando mis pasos.',
    'Hagamos un trato: yo pongo el talento, el ritmo y el plan perfecto, y tú te encargas del papeleo aburrido. Eso es lo que yo llamo una buena división del trabajo.',
    'Si vas a hablarme de deberes y obligaciones, que sea con un contrato por escrito en la mano. La pasión de una idol es real, ¡pero mis tarifas de asesora también lo son!',
    '¿Un nuevo encargo? Bien, pero que no sea como la última vez con Sunna. Tuve que trabajar el triple solo para evitar que destruyera el decorado antes del gran final.',
    '¡La coreografía de hoy va a ser intensa! Así que no quiero ver a nadie holgazaneando. Si no sudas la camiseta en los ensayos, no mereces compartir el escenario conmigo.'
]

# Función auxiliar para quitar acentos y tildes
def normalizar_texto(texto):
    texto = texto.lower()
    remplazos = (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"))
    for original, nuevo in remplazos:
        texto = texto.replace(original, nuevo)
    return texto

@bot.event
async def on_ready():
    print(f'Bot conectado con éxito como {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Normalizamos el mensaje (minúsculas y sin tildes)
    mensaje_limpio = normalizar_texto(message.content)

    # El regex busca la palabra "trabajo" de forma exacta e inmune a puntuación
    if re.search(r'\btrabajo\b', mensaje_limpio):
        frase_aleatoria = random.choice(FRASES_TRABAJO)
        await message.channel.send(frase_aleatoria)

    await bot.process_commands(message)

# ==========================================
# 3. ARRANQUE DEL SISTEMA
# ==========================================
if __name__ == "__main__":
    # 1. Arranca el servidor web Flask en segundo plano primero
    keep_alive()
    
    # 2. Inicia el bot leyendo el Token desde el entorno seguro de Render
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("ERROR: La variable DISCORD_TOKEN no está configurada en Render.")
    else:
        bot.run(TOKEN)

