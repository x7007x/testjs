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
