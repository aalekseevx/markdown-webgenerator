from flask import Flask, render_template, request, send_file
from os.path import join, exists
from datetime import datetime
from subprocess import run
from bs4 import BeautifulSoup
from settings import library_folder, path_to_chrome, temporary_files
from os import remove, makedirs

app = Flask(__name__)


def write_html(file):
    file.save('tmp/current.md')
    run(["grip", "tmp/current.md", "--export", "tmp/raw.html"])
    with open("tmp/raw.html") as f:
        raw_doc = f.read()

    soup = BeautifulSoup(raw_doc)
    article = str(soup.body.find('article'))
    with open("static/pref.txt") as pf:
        with open("static/suff.txt") as sf:
            with open("tmp/current.html", "w") as hf:
                hf.write(pf.read() + article + sf.read())


def clear_garbage():
    for file in temporary_files:
        remove(join('.', file))


def write_pdf(file):
    if not exists("tmp"):
        makedirs("tmp")
    if not exists("library"):
        makedirs("library")
    write_html(file)
    path = join(library_folder, datetime.now().strftime("%Y-%m-%d-%H:%M:%S")) + '.pdf'
    run([path_to_chrome, "--headless", "--no-sandbox", "-print-to-pdf=" + path, "tmp/current.html"])
    clear_garbage()
    return path


@app.route('/', methods=['GET'])
def index_get():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index_post():
    if 'file' not in request.files:
        return 'No file, no money.'
    path = write_pdf(request.files['file'])
    return send_file(path, mimetype='application/pdf')


if __name__ == '__main__':
    app.run()
