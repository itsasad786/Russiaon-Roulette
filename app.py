# app.py
from flask import Flask, request, jsonify
# from russian_roulette import run_game  # import your logic if in a separate file

app = Flask(__name__)

@app.get("/")
def health():
    return jsonify({"status": "ok"})

@app.post("/run")
def run():
    # Example: call your core function here
    # result = run_game(request.json or {})
    result = {"message": "Python ran on Render"}
    return jsonify(result)