from flask import Flask, request, render_template, redirect
import html
from functions import get_diff

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        file1 = request.files['file1']
        file2 = request.files['file2']

        if file1.filename == '' or file2.filename == '':
            return render_template('index.html', s='Error in Upload')

        s = get_diff(file1, file2)
        s = s.replace('\n', '<br>')

        return render_template('index.html', s=s)

    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)

