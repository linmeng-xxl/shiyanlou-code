from flask import Flask, render_template
import os, json
app = Flask(__name__)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    dir_path = '/home/project/files/'
    titles = []
    files = [dir_path + item for item in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, item))]
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            d = json.loads(f.read())
            titles.append(d['title'])
    return render_template('index.html', titles=titles)

@app.route('/files/<filename>')
def file(filename):
    file_path = '/home/project/files/' + filename + ".json"
    if os.path.exists(file_path):
        d = dict()
        with open(file_path, 'r', encoding='utf-8') as f:
            d = json.loads(f.read())
        return render_template('file.html', d=d)
    else:
        return not_found(None)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=1)
