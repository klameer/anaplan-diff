from flask import Flask, request, render_template
from functions import get_diff

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']

        if file1.filename == '' or file2.filename == '':
            return render_template('index.html', s='<p class="line del">Choose both files.</p>')

        s = get_diff(file1, file2, file1.filename, file2.filename)
        return render_template('index.html', s=s)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
