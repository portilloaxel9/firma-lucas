from flask import Flask, send_file
from PIL import Image, ImageDraw, ImageFont
import random
import io

app = Flask(__name__)

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
    """Genera una imagen con un mensaje aleatorio."""
    img = Image.new("RGB", (400, 100), color=(2, 3, 84))  # Fondo azul oscuro
    draw = ImageDraw.Draw(img)

    # Fuente (puedes usar una fuente TrueType en tu sistema)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    # Seleccionar mensaje aleatorio
    message = random.choice(messages)

    # Dibujar mensaje
    draw.text((20, 40), message, fill="white", font=font)

    # Guardar la imagen en un buffer
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
