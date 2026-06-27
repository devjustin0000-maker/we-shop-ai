from flask import Flask, render_template, request, redirect, url_for, session
import os
import json
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

app = Flask(__name__)
app.secret_key = "mysecretkey123"

# =====================
# CONFIG
# =====================
PASSWORD = "805090"
FOLDER_ID = "1n2JftVDn7SoEy_27ccIjXacNa1mDzI-J"

# =====================
# GOOGLE DRIVE SETUP
# =====================
credentials_info = json.loads(os.environ["GOOGLE_CREDENTIALS"])

credentials = service_account.Credentials.from_service_account_info(
    credentials_info,
    scopes=["https://www.googleapis.com/auth/drive"]
)

drive_service = build("drive", "v3", credentials=credentials)

# =====================
# LOGIN PAGE
# =====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return "<h2>❌ Wrong Password</h2><a href='/login'>Try Again</a>"

    return render_template("login.html")

# =====================
# HOME PAGE
# =====================
@app.route('/')
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html")

# =====================
# FILE UPLOAD
# =====================
@app.route('/upload', methods=['POST'])
def upload():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    file = request.files.get("file")

    if not file or file.filename == "":
        return "<h3>❌ No file selected</h3>"

    file_stream = io.BytesIO(file.read())

    media = MediaIoBaseUpload(
        file_stream,
        mimetype=file.content_type,
        resumable=True
    )

    metadata = {
        "name": file.filename,
        "parents": [FOLDER_ID]
    }

    drive_service.files().create(
        body=metadata,
        media_body=media,
        fields="id"
    ).execute()

    return f"""
    <h2>✅ Upload Successful!</h2>
    <p><b>{file.filename}</b> uploaded to Google Drive.</p>

    <br>

    <a href="/payment">
        <button>Pay ₹1</button>
    </a>

    <br><br>

    <a href="https://wa.me/919876543210" target="_blank">
        <button>Contact on WhatsApp</button>
    </a>
    """

# =====================
# PAYMENT PAGE
# =====================
@app.route('/payment')
def payment():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("payment.html")

# =====================
# LOGOUT
# =====================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

# =====================
# RENDER SAFE RUN
# =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
