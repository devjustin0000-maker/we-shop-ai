@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    prompt = request.form['prompt']

    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

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

    return "No file selected"
