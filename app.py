import os

from flask import Flask, render_template, request, make_response

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/label.js')
def label_js():
    return render_template('label.js')


@app.route('/app-browser.js')
def browser_js():
    return render_template('app-browser.js')


@app.route('/downloadData', methods=['POST'])
def generate_data():
    label_init = request.args.get('label_init')
    last_labeled = request.args.get('last_labeled')
    labels = request.args.get('labels').split(';')
    images = request.args.get('images').split(';')

    text = 'LAST_LABELED='+last_labeled+'\n'
    text += 'LABEL_INIT='+label_init+'\n'

    label_init = int(label_init)
    last_labeled = int(last_labeled)

    for i in range(label_init):
        text = text + '<image file="{}" state="corrected" text="{}" />\n'.format(images[i], labels[i])
        i += 1

    for i in range(label_init, last_labeled+1):
        text = text + '<image file="{}" state="corrected" text="{}" />\n'.format(images[i], labels[i])
        i += 1

    for i in range(last_labeled+1, len(images)):
        text = text + '<image file="{}" state="new" text="{}" />\n'.format(images[i], labels[i])
        i += 1

    text += '\n'
    response = make_response(text)
    response.headers['Content-Disposition'] = "attachment; filename='data.txt'"
    response.mimetype = 'text/plain'
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

