from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visit.db'
db = SQLAlchemy(app)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))        # 日付
    company = db.Column(db.String(100))    # タイトル
    name = db.Column(db.String(50))        # 場所（既存）
    purpose = db.Column(db.String(200))    # 順位（既存）
    rating = db.Column(db.Integer)         # 評価
    memo = db.Column(db.String(300))       # メモ

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    date = request.form['date']
    company = request.form['company']
    name = request.form['name']
    purpose = request.form['purpose']
    rating = request.form['rating']
    memo = request.form['memo']

    visit = Visit(
        date=date,
        company=company,
        name=name,
        purpose=purpose,
        rating=rating,
        memo=memo
    )
    db.session.add(visit)
    db.session.commit()
    return redirect('/list')

@app.route('/list')
def list_visits():
    sort = request.args.get('sort', 'none')

    if sort == 'rating_desc':
        visits = Visit.query.order_by(Visit.rating.desc()).all()
    elif sort == 'rating_asc':
        visits = Visit.query.order_by(Visit.rating.asc()).all()
    else:
        visits = Visit.query.all()

    return render_template('list.html', visits=visits)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)