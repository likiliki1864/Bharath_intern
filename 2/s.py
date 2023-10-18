from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_management.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='To Do')

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()
    return redirect('/')

@app.route('/update_task/<int:id>', methods=['POST'])
def update_task(id):
    task = Task.query.get(id)
    new_status = request.form['status']
    task.status = new_status
    db.session.commit()
    return redirect('/')

@app.route('/delete_task/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
