from flask import Flask
from models import db
from routes.user_routes import user_bp
from routes.transaction_routes import transaction_bp
from routes.dashboard_routes import dashboard_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register routes
app.register_blueprint(user_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(dashboard_bp)

@app.route('/')
def home():
    return {"message": "Backend Running Successfully"}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)