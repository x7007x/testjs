from flask import Flask, render_template
import subprocess
import os

app = Flask(__name__)

def build_obfuscated():
    input_file = "static/js/app.js"
    output_file = "static/js/app.obf.js"

    if not os.path.exists(output_file):
        try:
            subprocess.run([
                "npx",
                "javascript-obfuscator",
                input_file,
                "--output",
                output_file
            ], check=True)
        except Exception:
            pass

build_obfuscated()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/routes")
def list_routes():
    output = []

    for rule in app.url_map.iter_rules():
        methods = ",".join(sorted(rule.methods))
        line = f"{rule.rule}  [{methods}]"
        output.append(line)

    return "<br>".join(output)

import os

@app.route("/files")
def list_files():
    result = []

    for root, dirs, files in os.walk("."):
        for name in files:
            path = os.path.join(root, name)
            result.append(path)

    return "<br>".join(result)