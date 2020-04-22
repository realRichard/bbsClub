from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    flash,
)

from routes import current_user

from models.reply import Reply

from utils import log

main = Blueprint('reply', __name__)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    user = current_user()
    if user is not None:
        user_id = user.__dict__['id']
        new_reply = Reply.new(form, user_id=user_id)
        new_reply.hold()
    else:
        flash('登入后才能回复')
    return redirect(url_for('post.detail', id=form.get('post_id')))