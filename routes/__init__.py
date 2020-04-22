from flask import session

from models.user import User


def current_user():
    user_id = session.get('user_id', None)
    if user_id is not None:
        user = User.find_by(id=user_id)
        return user
    else:
        return None


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
