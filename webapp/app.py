import glob
import os

import pandas as pd

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

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
#curl "http://dam-obeu.iais.fraunhofer.de/results/021bd1fc-884c-4e34-9e36-022065d32e06"


@app.route('/outlier-dm-webapp/api/files', methods=['GET', 'POST'])
def api_files_list():
    if request.method == 'GET':
        files = existing_files()
        return jsonify(files)

    elif request.method == 'POST':
        print(request.get_json())
        data = request.get_json()

        full_filename = 'outputs/{}---{}.csv'.format(
            data['filename'],
            data['jobid'])
        pending_file = open(full_filename, 'w')
        pending_file.close()
        return jsonify(None)


@app.route('/outlier-dm-webapp/api/files/<path:filename>')
def api_file_detail(filename):
    json_answer = prepared_data(filename)
    return json_answer

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
