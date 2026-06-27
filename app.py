from flask import Flask, render_template, request, redirect, url_for, session
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

app = Flask(__name__)
app.secret_key = "mysecretkey123"

# Change this password
PASSWORD = "805090"

# Your Google Drive Folder ID
FOLDER_ID = "1n2JftVDn7SoEy_27ccIjXacNa1mDzI-J"

# Google Drive Setup
credentials_info = json.loads(os.environ["GOOGLE_CREDENTIALS"])

credentials = service_account.Credentials.from_service_account_info(
    credentials_info,
    scopes=["https://www.googleapis.com/auth/drive"]
)

drive_service = build("drive", "v3", credentials=credentials)

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return "<h2>Wrong Password!</h2><a href='/login'>Try Again</a>"

    return render_template("login.html")

# Home Page
@app.route('/')
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html")

# Upload
@app.route('/upload', methods=['POST'])
def upload():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    file = request.files.get("file")

    if not file or file.filename == "":
        return "No file selected."

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
    <p>{file.filename} has been saved to your Google Drive.</p>

    <br>

    <a href="/payment">
        <button>Pay ₹1</button>
    </a>
    """

# Payment Page
@app.route('/payment')
def payment():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("payment.html")

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
