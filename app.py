from flask import Flask, render_template, request
import os
from openai import OpenAI

app = Flask(__name__)
from flask import request, redirect

@app.before_request
def clean_url():
    if request.args.get("utm_source"):
        return redirect(request.path, code=301)

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
