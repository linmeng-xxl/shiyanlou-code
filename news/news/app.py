from flask import Flask, render_template
import os, json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/syl'
db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime, default=datetime.now())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'))
    content = db.Column(db.Text)
    
    def __repr__(self):
        return f'<File: {self.title}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __repr__(self):
        return f'<Category: {self.name}>'


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    files = [(f.id, f.title) for f in File.query.all()]
    return render_template('index.html', files=files)

@app.route('/files/<file_id>')
def file(file_id):
    file = File.query.filter_by(id=file_id).first()
    if file != None:
        category_name = Category.query.filter_by(id=file.category_id).first().name 
        return render_template('file.html', file=file, category_name=category_name)
    else:
        return not_found(None)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=1)
