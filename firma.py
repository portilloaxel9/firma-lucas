from flask import Flask, send_file
from PIL import Image, ImageDraw, ImageFont
import random
import io
import os

app = Flask(__name__)

# Ruta de la carpeta donde están las imágenes
STATIC_FOLDER = "static"

# Mensajes aleatorios
messages = [
    "Your energy use has just spiked. You'd better be careful.",
    "Do you canoe?",
    "You have been chosen. They will come soon.",
    "You're a (Spring, Summer, Autumn, Winter) and should decorate accordingly.",
    "The number 3 is very important in your life right now.",
    "Your psychic advisor suggests that you work on improving relationships.",
    "Your psychic advisor has had very strong vibrations from your Seventh House.",
    "Your psychic advisor suggests that you keep your secrets well this month.",
    "The drop off has been made. You've been warned.",
    "Your psychic advisor suggests that you plan your meetings carefully.",
    "The number 6 will be very important for you in the next 24 hours.",
    "Wrong number. Sorry.",
    "The end is near. Make preparations.",
    "The flashing light was just a test. You'll have plenty of warning next time.",
    "Your psychic advisor's head has just exploded. Be forewarned.",
    "They're coming soon. Maybe you should think twice about opening the door.",
    "We're fixing your phone line. Don't pick up the phone the next time it rings."
]

def generate_signature():
    """Genera una imagen con fondo azul, iconos y un mensaje aleatorio."""

    # Crear imagen con fondo azul
    background_color = (2, 3, 84)  # Azul oscuro
    img = Image.new("RGB", (400, 150), color=background_color)
    draw = ImageDraw.Draw(img)

    # Cargar imágenes de los íconos
    try:
        icon_path = os.path.join(STATIC_FOLDER, "face.png")
        button_path = os.path.join(STATIC_FOLDER, "phone.png")

        icon = Image.open(icon_path).resize((60, 60))  # Ícono de la máscara
        button = Image.open(button_path).resize((100, 40))  # Botón de teléfono

        # Pegamos las imágenes en la firma
        img.paste(icon, (20, 40), icon)
        img.paste(button, (250, 90), button)

    except Exception as e:
        print("Error cargando imágenes:", e)

    # Fuente para el texto (Arial)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()

    # Mensaje aleatorio
    message = random.choice(messages)

    # Dibujar mensaje con estilo (centrado, en itálica)
    text_x, text_y = 100, 50
    draw.text((text_x, text_y), message, fill="white", font=font)

    # Guardar imagen en un buffer
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return img_io

@app.route('/firma.png')
def signature():
    """Devuelve la firma en formato de imagen PNG."""
    return send_file(generate_signature(), mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
