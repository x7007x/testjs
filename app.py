from flask import Flask, render_template, Response
import subprocess
import shutil

app = Flask(__name__)

def run_obfuscator(js_code):
    possible_paths = [
        "node_modules/.bin/javascript-obfuscator",
        "./node_modules/.bin/javascript-obfuscator",
        shutil.which("javascript-obfuscator"),
        "npx javascript-obfuscator"
    ]

    for path in possible_paths:
        if not path:
            continue
        try:
            if "npx" in path:
                cmd = ["npx", "javascript-obfuscator"]
            else:
                cmd = [path]

            result = subprocess.run(
                cmd,
                input=js_code,
                text=True,
                capture_output=True
            )

            if result.stdout:
                return result.stdout
        except Exception:
            continue

    return js_code

@app.after_request
def obfuscate_js(response):
    if response.content_type.startswith("application/javascript"):
        js_code = response.get_data(as_text=True)
        response.set_data(run_obfuscator(js_code))
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/static/js/app.js")
def serve_js():
    with open("static/js/app.js", "r") as f:
        return Response(f.read(), mimetype="application/javascript")
