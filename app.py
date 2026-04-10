from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = 'uploads'
GRAPH_FOLDER = 'static/graphs'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create folders if not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GRAPH_FOLDER, exist_ok=True)


# Home + Upload route (MERGED)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # ---------------- DATA PROCESSING ----------------
            df = pd.read_csv(filepath)

            # Data Cleaning
            df.drop_duplicates(inplace=True)
            df.fillna("Missing", inplace=True)

            numeric_df = df.select_dtypes(include=['int64', 'float64'])

            # ---------------- GRAPHS ----------------

            # Histogram
            if not numeric_df.empty:
                numeric_df.hist(figsize=(8,6))
                plt.tight_layout()
                plt.savefig(f'{GRAPH_FOLDER}/histogram.png')
                plt.clf()

            # Bar Chart
            if not numeric_df.empty:
                numeric_df.iloc[:,0].value_counts().plot(kind='bar')
                plt.title("Bar Chart")
                plt.savefig(f'{GRAPH_FOLDER}/bar.png')
                plt.clf()

            # Heatmap
            if not numeric_df.empty:
                sns.heatmap(numeric_df.corr(), annot=True)
                plt.savefig(f'{GRAPH_FOLDER}/heatmap.png')
                plt.clf()

            # ---------------------------------------

            summary = df.describe().to_html()
            data = df.head().to_html()
            rows = df.shape[0]
            cols = df.shape[1]

            return render_template(
                'dashboard.html',
                tables=data,
                summary=summary,
                rows=rows,
                cols=cols
            )

    return render_template('index.html')


# Optional separate dashboard route (not required now)
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
