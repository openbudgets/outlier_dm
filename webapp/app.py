import os
import glob
import requests

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.debug = True


def existing_files():
    """
    Get a list of CSV files in the "outputs" folder.
    :return: list of strings representing file names.
    """
    files = []
    for file in glob.glob('outputs/*.csv'):
        if os.stat(file).st_size == 0:
            files.append({"filename": file, "status": "Processing"})
        else:
            files.append({"filename": file, "status": "Ready"})
    return files


def prepared_data(filename):
    """
    Read a CSV file and process its data to find columns with different names,
    build labels, etc.
    :param filename: String, name of the file to be read.
    :return: JSON string representing the data as a Pandas DataFrame.
    """
    import pandas as pd
    df = pd.DataFrame.from_csv(filename)

    # find out which columns represent budgetphase, year and target
    budgetphase_columns = list(filter(lambda col: 'budgetphase' in col.lower(),
                                      df.columns))
    if not budgetphase_columns:
        # we will use 'No Phase' as default because there's no much space on
        # screen to display something like Unknown Budget Phase
        df['budgetPhase'] = ['No Phase' for _ in range(len(df))]
    else:
        df['budgetPhase'] = df[budgetphase_columns[0]]

    columns_with_year = filter(lambda col: 'year' in col.lower(),
                               df.columns)
    year_columns = list(columns_with_year)
    if not year_columns:
        df['year'] = [1 for _ in range(len(df))]
    else:
        df['year'] = df[year_columns[0]]

    target_columns = list(filter(lambda col: 'target' in col.lower(),
                                 df.columns))
    df['Target'] = df[target_columns[0]]

    # rename columns
    sub_df = df[['year', 'budgetPhase', 'Target', 'Score']]
    sub_df.columns = ['x', 'color', 'y', 'size']

    # add score labels as a column to make the score human readable
    score_labels = ['Low', 'Medium', 'High']
    step = int((max(sub_df['size']))/3.0)
    sub_df['score_label'] = \
        pd.cut(sub_df['size'],
               range(0, int(max(sub_df['size'])) + step, step + 1),
               right=False,
               labels=score_labels)

    # transform the df to a json object so that it can be send back in response
    json_answer = sub_df.to_json(orient='records')
    return json_answer


def extract_jobid(file):
    """
    Take a dictionary containing filename and status of the file, then extract
    the job id from the filename string
    :param file: Dictionary, contains *filename* and *status*
    :return: String representing the job id of the DAM request
    """
    filename = file['filename']
    jobid_position = 3 + filename.find('---')
    file_extension_len = 4
    return filename[jobid_position: -file_extension_len]


def query_dam(file):
    """
    Send a GET HTTP request to DAM to access the results of a dataset.
    The results will be placed inside the file.
    :param file: dictionary containing the *filename* and *status*
    :return: None
    """
    import pandas as pd
    jobid = extract_jobid(file)
    print("Querying DAM for jobid {}".format(jobid))

    response = requests.get(
        'http://dam-obeu.iais.fraunhofer.de/results/{}'.format(jobid))

    if response.status_code != 200:
        print('Bad response code: {}'.format(response.status_code))
        return
    if response.json().get('result') is None:
        return
    if response.json().get('result').get('result') is None:
        return

    df = pd.DataFrame.from_records(response.json()['result']['result'])
    df.to_csv('{}'.format(file['filename']))


def is_processing(file):
    return file['status'] == 'Processing'


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


@app.route('/outlier-dm-webapp/api/files', methods=['GET', 'POST'])
def api_files_list():
    if request.method == 'GET':
        files = existing_files()
        pending_files = filter(is_processing, files)
        list(map(query_dam, pending_files))
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
        return jsonify(True)


@app.route('/outlier-dm-webapp/api/files/<path:filename>')
def api_file_detail(filename):
    json_answer = prepared_data(filename)
    return json_answer

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
