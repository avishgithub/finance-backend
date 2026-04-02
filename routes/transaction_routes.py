from flask import request, Blueprint
from models import db, Transaction
from utils.role_checker import check_role

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/transactions', methods=['POST'])
def create_transaction():
    if not check_role(['admin']):
        return {"error": "Access denied"}, 403

    data = request.json

    if not data:
        return {"error": "Invalid JSON input"}, 400

    if data['amount'] <= 0:
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


@transaction_bp.route('/transactions', methods=['GET'])
def get_transactions():
    type_filter = request.args.get('type')

    query = Transaction.query

    if type_filter:
        query = query.filter_by(type=type_filter)

    transactions = query.all()

    return [{
        "id": t.id,
        "amount": t.amount,
        "type": t.type,
        "category": t.category,
        "date": t.date,
        "notes": t.notes
    } for t in transactions]

@transaction_bp.route('/transactions/<int:id>', methods=['PUT'])
def update_transaction(id):
    if not check_role(['admin']):
        return {"error": "Access denied"}, 403

    data = request.json

    if not data:
        return {"error": "Invalid JSON input"}, 400

    t = Transaction.query.get(id)

    if not t:
        return {"error": "Transaction not found"}, 404

    # Update fields
    t.amount = data.get('amount', t.amount)
    t.type = data.get('type', t.type)
    t.category = data.get('category', t.category)
    t.date = data.get('date', t.date)
    t.notes = data.get('notes', t.notes)

    db.session.commit()

    return {"message": "Transaction updated successfully"}

@transaction_bp.route('/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    if not check_role(['admin']):
        return {"error": "Access denied"}, 403

    t = Transaction.query.get(id)

    if not t:
        return {"error": "Transaction not found"}, 404

    db.session.delete(t)
    db.session.commit()

    return {"message": "Transaction deleted successfully"}