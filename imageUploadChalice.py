from chalice import Chalice, CORSConfig
from PIL import Image
from io import BytesIO
import boto3
import cgi
import random
import string
import time

app = Chalice(app_name='imageupload')
app.api.binary_types.append('multipart/form-data')
cors_config = CORSConfig(
        allow_origin="*",
        allow_headers=["Content-Type"]
        )

_ALLOWED_ORIGINS = set([
    "https://www.paytime.co.kr",
    "http://test.paytime.co.kr"
    ])

@app.route('/')
def index():
    return {'hello': 'world'}

def _get_parts(file_field="file"):
    request_body = app.current_request._body
    body = app.current_request.raw_body

    content_type_header = app.current_request.headers['content-type']
    content_type, property_dict = cgi.parse_header(content_type_header)

    property_dict['boundary'] = bytes(property_dict['boundary'], "utf-8")
    form_data = cgi.parse_multipart(BytesIO(body), property_dict)
    ext = 'png'
    extracted_image = form_data[file_field][0]

    return extracted_image

def get_random_string(length=10):
    _random = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    return _random

@app.route("/upload", methods=["POST"], content_types=['multipart/form-data'], cors=cors_config)
def upload():
    origin = app.current_request.to_dict()["headers"].get("origin", "")
    if origin not in _ALLOWED_ORIGINS and origin != "" and origin.startswith("http"):
        return {"fuckyou": "fuckyou", "origin": origin}

    files = _get_parts()
    _file = BytesIO(files)
    image = Image.open(_file)
    sessionkey = get_random_string(length=7)
    filename = "%s_%s.jpg" % (sessionkey, str(time.time()).replace('.','_'))
    save_img = BytesIO()
    _format = image.format
    width, height = image.size
    ratio = width/height
    if(ratio >= 1 and width > 1000):
        width = 1000
        height = int(1000 / ratio)
        image = image.resize((width, height), Image.ANTIALIAS)
    elif(ratio < 1 and height > 800):
        height = 800
        width = int(800 * ratio)
        image = image.resize((width, height), Image.ANTIALIAS)

    try:
        image_exif = image._getexif()
        image_orientation = image_exif[274]
        if image_orientation == 3:
            image = image.rotate(180)
        elif image_orientation == 6:
            image = image.rotate(-90)
        elif image_orientation == 8:
            image = image.rotate(90)

    except Exception as e:
        pass

    image.save(save_img, format=_format, quality=80)
    save_img.seek(0)
    client = boto3.client("s3")
    client.put_object(
            Bucket=".file",
            Key="cover/temp/%s" % (filename,),
            Body=save_img,
            ContentType="image/jpeg")
    url = "https://s3-us-west-2.amazonaws.com//temp/%s" % (filename,)
    res = {
            "file_name" : filename,
            "url": url
            }

    return res

@app.route("/chat", methods=["POST"], content_types=['multipart/form-data'], cors=cors_config)
def chatImage():
    origin = app.current_request.to_dict()["headers"].get("origin", "")
    if origin not in _ALLOWED_ORIGINS and origin != "" and origin.startswith("http"):
        return {"fuckyou": "fuckyou", "origin": origin}

    files = _get_parts("image")
    _file = BytesIO(files)
    image = Image.open(_file)
    sessionkey = get_random_string(length=7)
    filename = "%s_%s.jpg" % (sessionkey, str(time.time()).replace('.','_'))
    save_img = BytesIO()
    _format = image.format
    image.save(save_img, format=_format, quality=70)
    save_img.seek(0)
    client = boto3.client("s3")
    client.put_object(
            Bucket=".file",
            Key="chat/%s" % (filename,),
            Body=save_img,
            ContentType="image/jpeg")
    url = "https://file.paytime.co.kr/chat/%s" % (filename,)
    res = {
            "file_name" : filename,
            "url": url
            }

    return res

