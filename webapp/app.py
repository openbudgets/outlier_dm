import glob
import os

import pandas as pd

from flask import Flask, render_template, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.debug = True


def existing_files():
    files = []
    for file in glob.glob('outputs/*.csv'):
        if os.stat(file).st_size == 0:
            files.append({"filename": file, "status": "Processing"})
        else:
            files.append({"filename": file, "status": "Ready"})
    return files


def prepared_data(filename):
    df = pd.DataFrame.from_csv(filename)
    sub_df = df[['year', 'budgetPhase', 'Target', 'Score']]
    sub_df.columns = ['x', 'color', 'y', 'size']
    json_answer = sub_df.to_json(orient='records')
    return json_answer


@app.route('/outlier-dm-webapp/<path:filename>')
def file_detail(filename):
    json_answer = prepared_data(filename)

    return render_template(
        'detail.html',
        data=json_answer
    )


@app.route('/outlier-dm-webapp')
def index():
    files = existing_files()
    return render_template(
        'list.html',
        files=files
    )


@app.route('/outlier-dm-webapp/api/files')
def api_files_list():
    files = existing_files()
    return jsonify(files)


@app.route('/outlier-dm-webapp/api/files/<path:filename>')
def api_file_detail(filename):
    json_answer = prepared_data(filename)
    return json_answer

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
