from flask import Flask, jsonify
from vercel_helpers import VercelRequest, VercelResponse # Note: This library might be needed for Flask 
                                                            # with Vercel deployment configurations.

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello from Python!"})
