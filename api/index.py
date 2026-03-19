from flask import Flask, render_template, Response
import subprocess

app = Flask(__name__)

@app.after_request
def obfuscate_js(response):
    if response.content_type.startswith("application/javascript"):
        try:
            result = subprocess.run(
                ["node_modules/.bin/javascript-obfuscator"],
                input=response.get_data(as_text=True),
                text=True,
                capture_output=True
            )
            if result.stdout:
                response.set_data(result.stdout)
        except Exception:
            pass
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/static/js/app.js")
def serve_js():
    with open("static/js/app.js", "r") as f:
        return Response(f.read(), mimetype="application/javascript")
