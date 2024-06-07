from flask import Flask
from flask import json
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    data_excel = pd.read_excel('Dados.xlsx', sheet_name='Sheet1')
    data_json = data_excel.to_json(orient='records')

    return json.loads(data_json)

if __name__ == '__main__':
    app.run(debug=True)
