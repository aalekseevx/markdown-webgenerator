from flask import Flask, render_template, request, redirect
from os.path import join
from datetime import datetime
from subprocess import run
from bs4 import BeautifulSoup
from settings import library_folder, path_to_chrome
app = Flask(__name__)


def get_html():
    run(["grip", "current.md", "--export", "current.html"])
    with open("current.html") as f:
        raw_doc = f.read()

    soup = BeautifulSoup(raw_doc)
    article = str(soup.body.find('article'))
    with open("static/pref.txt") as pf:
        with open("static/suff.txt") as sf:
            resp = pf.read() + article + sf.read()
            return resp


def write_pdf(file):
    file.save('./current.md')
    path = join(library_folder, datetime.now().strftime("%Y-%m-%d-%H:%M:%S")) + '.pdf'
    run([path_to_chrome, "--headless", "--no-sandbox", "-print-to-pdf=" + path, "current.html"])


@app.route('/', methods=['GET'])
def index_get():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index_post():
    if 'file' not in request.files:
        return 'No file, no money.'
    write_pdf(request.files['file'])
    return "All done, sir."


if __name__ == '__main__':
    app.run()
