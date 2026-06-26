from flask import Flask, render_template, request
import os
from openai import OpenAI

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🔴 PUT YOUR REAL OPENAI KEY HERE
client = OpenAI(api_key="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")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/payment')
def payment():
    return render_template('payment.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    prompt = request.form['prompt']

    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            ai_result = response.choices[0].message.content

            return f"""
            <h2>Upload Successful</h2>
            <p><b>Your Prompt:</b> {prompt}</p>
            <p><b>AI Response:</b> {ai_result}</p>
            """

        except Exception as e:
            return f"<h2>AI Error:</h2><p>{e}</p>"

    return "No file selected"


if __name__ == '__main__':
    app.run(debug=True)
