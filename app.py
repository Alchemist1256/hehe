from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tedx_27iq_user:jUVHT7tYZ0jzUcTNhDiVl4FGX2WLiYZQ@dpg-d3v6osbipnbc739einfg-a.oregon-postgres.render.com/tedx_27iq'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model for counting Yes clicks
class YesCounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables once at startup
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    if data and data.get('response') == 'Yes':
        new_entry = YesCounter()
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({'status':'success'})
    return jsonify({'status':'ignored'}), 400

@app.route('/admin')
def admin():
    count = YesCounter.query.count()
    return render_template('admin.html', count=count)

if __name__ == '__main__':
    app.run(debug=True)
