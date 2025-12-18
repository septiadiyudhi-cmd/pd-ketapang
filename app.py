from flask import Flask, render_template, request, redirect
import requests
import os
import json
from datetime import datetime

app = Flask(__name__)

# pastikan folder ada
os.makedirs("data", exist_ok=True)
os.makedirs("data/generated_pages", exist_ok=True)

DATABASE = "data/warnings.json"

# buat file database jika belum ada
if not os.path.exists(DATABASE):
    with open(DATABASE, "w") as f:
        json.dump([], f, indent=4)


@app.route("/")
def home():
    return redirect("/create")


@app.route("/create")
def create():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    # Ambil data dari form
    location = request.form.get("location")
    forecaster = request.form.get("forecaster")
    initial_time = request.form.get("initial_time")
    valid_until = request.form.get("valid_until")
    narr = request.form.get("narration")

    # Buat ID warning
    # Contoh: ktpgglmn_202512151930
    dt = datetime.now().strftime("%Y%m%d%H%M")
    warning_id = f"ktpgglmn_{dt}"

    # Simpan ke database JSON
    with open(DATABASE, "r") as f:
        db = json.load(f)

    entry = {
        "id": warning_id,
        "location": location,
        "forecaster": forecaster,
        "initial_time": initial_time,
        "valid_until": valid_until,
        "narration": narr
    }

    db.append(entry)

    with open(DATABASE, "w") as f:
        json.dump(db, f, indent=4)

    # Generate halaman warning HTML
    output_path = f"data/generated_pages/{warning_id}.html"
    html = render_template("warning_page.html", **entry)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    # Redirect user ke halaman warning
    return redirect(f"/warning/{warning_id}")


@app.route("/warning/<wid>")
def warning(wid):
    file_path = f"data/generated_pages/{wid}.html"
    if not os.path.exists(file_path):
        return "Warning not found", 404

    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    return html


if __name__ == "__main__":
    app.run(debug=True)

