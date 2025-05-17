from flask import Flask, render_template, request, jsonify
from routes import list_interfaces, get_game_prefixes, apply_routes

app = Flask(__name__)

@app.route('/')
def home():
    games = {"Riot":"6507"}
    return render_template("index.html", games=games, interfaces=list_interfaces())

@app.route('/apply', methods=['POST'])
def apply():
    asn = request.form.get("asn")
    gateway = request.form.get("gateway")

    prefixes = get_game_prefixes(asn)

    success = apply_routes(prefixes, gateway)

    return render_template("apply.html", success=success, prefixes=prefixes)