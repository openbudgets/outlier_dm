import glob
import os

import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)
app.debug = True


@app.route('/outlier-dm-webapp/<path:filename>')
def detail(filename):
    print(filename)
    df = pd.DataFrame.from_csv(filename)
    sub_df = df[['year', 'budgetPhase', 'Target', 'Score']]
    sub_df.columns = ['x', 'color', 'y', 'size']

    return render_template(
        'detail.html',
        data=sub_df.to_json(orient='records')
    )


@app.route('/outlier-dm-webapp')
def index():
    files = []

    for file in glob.glob('outputs/*.csv'):
        if os.stat(file).st_size == 0:
            files.append({"filename": file, "status": "Processing"})
        else:
            files.append({"filename": file, "status": "Ready"})

    return render_template(
        'list.html',
        files=files
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
