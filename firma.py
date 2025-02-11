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
    "You're a Spring and should decorate accordingly.",
    "You're a Summer and should decorate accordingly.",
    "You're an Autumn and should decorate accordingly.",
    "You're a Winter and should decorate accordingly.",
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

def draw_text_with_wrap(draw, text, position, font, max_width):
    """Dibuja texto con ajuste automático de línea usando textbbox()"""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        text_bbox = draw.textbbox((0, 0), test_line, font=font)  # Calcula tamaño del texto
        text_width = text_bbox[2] - text_bbox[0]  # Ancho del texto

        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)

    x, y = position
    total_height = 0
    for line in lines:
        draw.text((x, y), line, fill="white", font=font)
        line_height = draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1]
        y += line_height + 2  # Espaciado entre líneas
        total_height += line_height + 2

    return total_height

def generate_signature():
    """Genera una imagen con fondo azul, iconos y un mensaje aleatorio."""
    
    # Configuración general
    background_color = (2, 3, 84)  # Azul oscuro
    width, height = 400, 150  # Ajuste para mantener la proporción correcta
    padding = 15  # Espaciado del contenedor

    img = Image.new("RGB", (width, height), color=background_color)
    draw = ImageDraw.Draw(img)

    # Cargar imágenes de los íconos
    try:
        icon_path = os.path.join(STATIC_FOLDER, "face.png")
        button_path = os.path.join(STATIC_FOLDER, "phone.png")

        icon = Image.open(icon_path).resize((60, 60))  # Ajuste para mejor alineación
        button = Image.open(button_path).resize((100, 35))  # Tamaño fijo del botón

        # Pegamos la imagen del icono a la izquierda (centrado verticalmente)
        icon_x = padding
        icon_y = (height // 2 - icon.height // 2) - 10  # Se sube un poco para compensar el texto
        img.paste(icon, (icon_x, icon_y), icon)

    except Exception as e:
        print("Error cargando imágenes:", e)

    try:
        font_path = os.path.join(STATIC_FOLDER, "ComicSansMS3.ttf")  # Ruta correcta
        font = ImageFont.truetype(font_path, 14)  # Tamaño de la fuente
    except:
        font = ImageFont.load_default()

    # Mensaje aleatorio
    message = random.choice(messages)

    # Posición del texto (centrado entre el icono y el botón)
    text_x = 110  # Ajuste para alinearlo con el icono
    text_y = 40
    max_text_width = 200  # El texto se ajusta a este ancho
    text_height = draw_text_with_wrap(draw, message, (text_x, text_y), font, max_text_width)

    # Ajustar la posición del botón para que quede centrado debajo del texto
    button_x = (width - button.width) // 2  # Centrado horizontalmente
    button_y = text_y + text_height + 10  # Se coloca debajo del texto con margen
    button_y = 180

    # Pegamos la imagen del botón en su posición correcta
    try:
        img.paste(button, (button_x, button_y), button)
    except Exception as e:
        print("Error pegando el botón:", e)

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
