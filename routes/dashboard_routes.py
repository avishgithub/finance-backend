from flask import Blueprint
from sqlalchemy import func
from models import db, Transaction
from utils.role_checker import check_role

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
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