from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')
    
    @app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        return f'''
        <h2>Upload Successful!</h2>
        <img src="/uploads/{file.filename}" width="400">
        <br><br>
        <a href="/">Upload Another Image</a>
        '''

    return "No file selected"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Payment page
@app.route('/payment')
def payment():
    return render_template('payment.html')
    @app.route('/payment')
def payment():
    return render_template('payment.html')

if __name__ == '__main__':
    app.run(debug=True)
