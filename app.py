from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "mysecretkey123"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Change this password to anything you want
PASSWORD = "805090"

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return "<h2>Wrong Password!</h2><a href='/login'>Try Again</a>"

    return render_template('login.html')

# Home Page
@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

# Upload File
@app.route('/upload', methods=['POST'])
def upload():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    file = request.files['file']

    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        return f"""
        <h2>Upload Successful!</h2>
        <p>File: {file.filename}</p>

        <br>

        <a href="/payment">
            <button>Pay ₹1</button>
        </a>
        """

    return "No file selected."

# Payment Page
@app.route('/payment')
def payment():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('payment.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
