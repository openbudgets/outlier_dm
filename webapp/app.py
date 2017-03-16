import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    df = pd.DataFrame.from_csv('Result_top25.csv')
    sub_df = df[['year', 'budgetPhase', 'Target', 'Score']]
    sub_df.columns = ['x', 'color', 'y', 'size']

    return render_template(
        'index.html',
        data=sub_df.to_json(orient='records')
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
