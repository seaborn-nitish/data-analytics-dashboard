from flask import Flask, render_template, request
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

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

    # Select numeric columns
    numeric_df = df.select_dtypes(include=['int64', 'float64'])

    # ------------------ GRAPHS ------------------

    # Histogram
    if not numeric_df.empty:
        numeric_df.hist(figsize=(8,6))
        plt.tight_layout()
        plt.savefig('static/graphs/histogram.png')
        plt.clf()

    # Bar chart (first column)
    if not numeric_df.empty:
        numeric_df.iloc[:,0].value_counts().plot(kind='bar')
        plt.title("Bar Chart")
        plt.savefig('static/graphs/bar.png')
        plt.clf()

    # Heatmap
    if not numeric_df.empty:
        sns.heatmap(numeric_df.corr(), annot=True)
        plt.savefig('static/graphs/heatmap.png')
        plt.clf()

    # -------------------------------------------

    # Summary + preview
    summary = df.describe().to_html()
    data = df.head().to_html()

    return f"""
    <h2>File Uploaded Successfully!</h2>

    <h3>First 5 Rows:</h3>
    {data}

    <h3>Summary:</h3>
    {summary}

    <h3>Graphs:</h3>
    <img src="/static/graphs/histogram.png" width="400">
    <img src="/static/graphs/bar.png" width="400">
    <img src="/static/graphs/heatmap.png" width="400">
    """

if __name__ == '__main__':
    app.run(debug=True)
