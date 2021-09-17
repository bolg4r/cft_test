from flask import Flask, render_template, request
import cv2
import numpy as np
from PIL import Image, ImageColor




#почистить код
#чекнуть проо тесты
#чекнуть про зависимости
# json логирование
#
#

app = Flask(__name__)
app.config['IMAGE_UPLOADS'] = 'static/image'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG"]



def img_to_np(image):
    img = Image.open(image)
    img = np.array(img)
    return cv2.resize(img, (224, 224))


def hex_to_rgb(hex_code):
    return ImageColor.getcolor(hex_code, 'RGB')


def count_color(img, code):
    return cv2.countNonZero(cv2.inRange(img, code, code))


def black_white(img):
    white = np.array([255, 255, 255], np.uint8)
    black = np.array([0, 0, 0], np.uint8)
    black_amount = count_color(img, black)
    white_amount = count_color(img, white)
    if black_amount > white_amount:
        return 'Black pixels more then white ones'
    elif black_amount < white_amount:
        return'White pixels more then black ones'
    else:
        return 'Number of white and black pixels is the same'


def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if request.files:
            image = request.files['image']
            if allowed_image(image.filename):
                image = img_to_np(image)
            else:
                return render_template('index.html', error='It is not an image')
            if request.form.get('hex_code'):
                code = hex_to_rgb(request.form.get('hex_code'))
                return render_template('index.html', result=black_white(image), hex_result=count_color(image, code))
            return render_template('index.html', result=black_white(image))
    return render_template('index.html' )


if __name__ == '__main__':
    app.run('127.0.0.1', port=1337)
