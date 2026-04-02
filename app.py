from flask import request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def home():
    return {"message": "Backend Running Successfully"}


# ---------------- MODELS ---------------- #

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    role = db.Column(db.String(20))
    status = db.Column(db.String(20))


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    type = db.Column(db.String(10))
    category = db.Column(db.String(50))
    date = db.Column(db.String(20))
    notes = db.Column(db.String(100))


# ---------------- USER APIs ---------------- #

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json

    if not data:
        return {"error": "Invalid JSON input"}, 400

    if not data.get('name') or not data.get('email') or not data.get('role'):
        return {"error": "Missing required fields"}, 400
    
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return {"error": "User already exists"}, 400
    
    user = User(
        name=data['name'],
        email=data['email'],
        role=data['role'],
        status='active'
    )

    db.session.add(user)
    db.session.commit()

    return {"message": "User created successfully"}, 201


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()

    result = []
    for u in users:
        result.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role,
            "status": u.status
        })

    return result


# ---------------- TRANSACTION APIs ---------------- #

@app.route('/transactions', methods=['POST'])
def create_transaction():
    if not check_role(['admin']):
        return {"error": "Access denied"}, 403

    data = request.json

    if not data:
        return {"error": "Invalid JSON input"}, 400

    if data['amount'] <=0:
        return {"error": "Amount must be greater than 0"}, 400
    
    if data['type'] not in ['income', 'expense']:
        return {"error": "Invalid type"}, 400
    
    t = Transaction(
        amount=data['amount'],
        type=data['type'],
        category=data['category'],
        date=data['date'],
        notes=data.get('notes', '')
    )

    db.session.add(t)
    db.session.commit()
    return {"message": "Transaction added successfully"}, 201


@app.route('/transactions', methods=['GET'])
def get_transactions():
    type_filter = request.args.get('type')

    query = Transaction.query

    if type_filter:
        query = query.filter_by(type=type_filter)

    transactions = query.all()

    result = []
    for t in transactions:
        result.append({
            "id": t.id,
            "amount": t.amount,
            "type": t.type,
            "category": t.category,
            "date": t.date,
            "notes": t.notes
        })

    return result


# ---------------- ROLE CHECKER ---------------- #

def check_role(allowed_roles):
    role = request.headers.get('role')

    if not role:
        return False
    
    if role not in allowed_roles:
        return False
    
    return True


# ---------------- DASHBOARD API ---------------- #

from sqlalchemy import func

@app.route('/dashboard', methods=['GET'])
def dashboard():

    if not check_role(['admin', 'analyst']):
        return {"error": "Access denied"}, 403

    income = db.session.query(func.sum(Transaction.amount)).filter_by(type='income').scalar() or 0
    expense = db.session.query(func.sum(Transaction.amount)).filter_by(type='expense').scalar() or 0

    return {
        "total_income": income,
        "total_expense": expense,
        "net_balance": income - expense
    }


# ---------------- MAIN ---------------- #

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
