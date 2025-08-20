import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/health")
def health():
    return "ok", 200

@app.route("/")
def home():
    return render_template("registro.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
