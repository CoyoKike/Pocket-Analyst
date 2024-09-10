from flask import Flask, request, render_template
from pandas_profiling import ProfileReport
import pandas as pd
import os

app = Flask(__name__)


@app.route('/')
def upload_file():
    return render_template('upload.html')


@app.route('/process', methods=['POST'])
def process_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_ext = os.path.splitext(uploaded_file.filename)[1]
        if file_ext not in ['.csv', '.xlsx']:
            return "Invalid file format. Please upload a CSV or XLSX file."
        df = pd.read_csv(uploaded_file) if file_ext == '.csv' else pd.read_excel(
            uploaded_file)
        # Set minimal=True to exclude missing values
        profile = ProfileReport(df, minimal=True)
        profile.to_file("static/profile_report.html")
        return render_template('result.html', profile_url='/static/profile_report.html')
    else:
        return "No file uploaded."


if __name__ == '__main__':
    app.run(debug=True)
