from flask import Flask

from flask_wtf.csrf import CSRFProtect

from config import (
    config,
    secret_key,
)

from utils import log

from routes.index import main as index_routes
from routes.auth import main as auth_routes
from routes.post import main as post_routes
from routes.reply import main as reply_routes
from routes.user import main as user_routes
from routes.admin import main as admin_routes
from routes.mail import main as mail_routes


app = Flask(__name__)
CSRFProtect(app)
app.secret_key = secret_key
# close csrf
# app.config['WTF_CSRF_ENABLED'] = False

app.register_blueprint(index_routes)
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(post_routes, url_prefix='/post')
app.register_blueprint(reply_routes, url_prefix='/reply')
app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(admin_routes, url_prefix='/admin')
app.register_blueprint(mail_routes, url_prefix='/mail')


if __name__ == '__main__':
    app.run(**config)