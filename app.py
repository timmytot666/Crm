from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login' # Assuming 'users' blueprint and 'login' route

# Import and register blueprints
from users.routes import users_bp
from contacts.routes import contacts_bp
from companies.routes import companies_bp
from deals.routes import deals_bp
from activities.routes import activities_bp
from main.routes import main_bp

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(contacts_bp, url_prefix='/contacts')
app.register_blueprint(companies_bp, url_prefix='/companies')
app.register_blueprint(deals_bp, url_prefix='/deals')
app.register_blueprint(activities_bp, url_prefix='/activities')
app.register_blueprint(main_bp) # No prefix for general routes like search

if __name__ == '__main__':
    app.run(debug=True)
