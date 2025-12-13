# app.py
from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DRAWINGS_FILE = 'drawings.json'

# Initialize the drawings file if it doesn't exist
if not os.path.exists(DRAWINGS_FILE):
    with open(DRAWINGS_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/canvas')
def canvas():
    return render_template('canvas.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/save_drawing', methods=['POST'])
def save_drawing():
    data = request.json
    with open(DRAWINGS_FILE, 'r+') as f:
        drawings = json.load(f)
        drawings.append(data)
        f.seek(0)
        f.truncate()
        json.dump(drawings, f)
    return jsonify({'status': 'ok'})

@app.route('/get_drawings')
def get_drawings():
    with open(DRAWINGS_FILE, 'r') as f:
        drawings = json.load(f)
    return jsonify(drawings)

@app.route('/delete_drawing/<int:index>', methods=['DELETE'])
def delete_drawing(index):
    try:
        with open(DRAWINGS_FILE, 'r+') as f:
            drawings = json.load(f)
            if 0 <= index < len(drawings):
                del drawings[index]
                f.seek(0)
                f.truncate()
                json.dump(drawings, f)
                return jsonify({'status': 'ok'})
            else:
                return jsonify({'status': 'error', 'message': 'Invalid index'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)