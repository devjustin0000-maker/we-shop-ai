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
