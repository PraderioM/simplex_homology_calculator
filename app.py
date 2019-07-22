import os

from flask import Flask, render_template, request

from input_output import read_raw_data, get_homology_groups_formatted_text
from mathematics import get_homology_groups

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/label.js')
def label_js():
    return render_template('label.js')


@app.route('/readData', methods=['POST'])
def generate_data():
    # Maximal faces are the only element sent by the form.
    maximal_faces = ''
    for data in request.form:
        maximal_faces = data

    # Make computations.
    maximal_faces = read_raw_data(raw_data=maximal_faces)
    homology_groups = get_homology_groups(faces=maximal_faces)
    text = get_homology_groups_formatted_text(homology_groups=homology_groups)

    return text


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

