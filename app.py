from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Read CSV
    df = pd.read_csv(filepath)

    # Data Cleaning
    df.drop_duplicates(inplace=True)
    df.fillna("Missing", inplace=True)

    # Summary
    summary = df.describe().to_html()

    # First 5 rows
    data = df.head().to_html()

    return f"""
    <h2>File Uploaded Successfully!</h2>
    <h3>First 5 Rows:</h3>
    {data}
    <h3>Summary Statistics:</h3>
    {summary}
    """

if __name__ == '__main__':
    app.run(debug=True)
git add .
git commit -m "Added data cleaning and summary"
git push