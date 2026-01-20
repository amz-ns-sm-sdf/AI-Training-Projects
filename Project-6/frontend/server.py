from flask import Flask, send_file
import os

app = Flask(__name__)
app.config['STATIC_FOLDER'] = os.path.dirname(__file__)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_file(filename)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3005, debug=False, use_reloader=False)
