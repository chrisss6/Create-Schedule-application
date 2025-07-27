from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql://postgres:password@db:5432/choseisan')
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        date = request.form.get('date')
        if title and date:
            event = Event(title=title, date=date)
            db.session.add(event)
            db.session.commit()
        return redirect('/')
    events = Event.query.all()
    return render_template('index.html', events=events)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
