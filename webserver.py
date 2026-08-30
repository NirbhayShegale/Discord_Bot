from flask import Flask, request, jsonify
from threading import Thread

app = Flask("")

@app.route('/chat')
def home():
    return "Post is working!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()