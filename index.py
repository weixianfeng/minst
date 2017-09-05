from flask import Flask
from flask import render_template, Response, request
from tf.identify_image import get_code
import json


app = Flask(__name__)

@app.route("/")
def hello():
    return "hello world!"


@app.route('/uploadd', methods=['POST'])
def post_upload_form():
    f = request.files['img']
    data = {
        "result": str(get_code(f))
    }
    return Response(json.dumps(data), mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
