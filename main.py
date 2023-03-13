from flask import Flask, render_template, request
import io
from PIL import Image, ImageDraw, ImageFont
import random
import string
from base64 import b64encode


app = Flask(__name__)


@app.route('/', methods=['GET'])  # To render Homepage
def home_page():
    image, text = create_image()
    file_object = io.BytesIO()
    image.save(file_object, 'PNG')
    base64img = "data:image/png;base64," + \
        b64encode(file_object.getvalue()).decode('ascii')
    return render_template('index.html', base64img=base64img, check_text=text)


@app.route('/', methods=['POST'])
def check_captcha():
    input_text = request.form.get('input_text')
    check_text = request.form.get('check_text')
    if input_text.lower() == check_text.lower():
        message = 'SUCCESS'
    else:
        message = 'FAIL'
    return render_template('index.html', message=message)


def create_image():
    # create a new image with a orange background
    width, height = 200, 100
    image = Image.new("RGB", (width, height), "orange")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    text = "".join(random.choices(
        string.ascii_letters + string.digits, k=8))
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) / 2
    y = (height - text_height) / 2
    draw.text((x, y), text, font=font, fill=(0, 0, 0))

    # add random lines to image
    for i in range(random.randint(1, 3)):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=(0, 0, 0), width=2)

    return image, text


if __name__ == "__main__":
    app.run(debug=True)
