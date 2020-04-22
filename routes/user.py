from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    send_from_directory,
    redirect,
    abort,
)

from models.user import User
from models.post import Post
from models.reply import Reply

import os

from werkzeug.utils import secure_filename

from config import upload_folder

from utils import log

from routes import (
    allowed_file,
    current_user,
)


main = Blueprint('user', __name__)

@main.route('/<string:username>')
def index(username):
    user = User.find_by(username=username)
    if user is not None:
        is_self = bool(current_user() is not None and current_user().id == user.id)
        posts = Post.find_all(user_id=user.id)
        replies = Reply.find_all(user_id=user.id)
        return render_template('user/profile.html', user=user, is_self=is_self, posts=posts, replies=replies)
    else:
        return abort(404)


@main.route('/signature/update', methods=['POST'])
def update_signature():
    form = request.form
    user = User.find_by(id=int(form.get('id')))
    if user is not None:
        user.signature = form.get('signature', user.signature)
        user.hold()
    return redirect(url_for('.index', username=user.username))


@main.route('/headportrait/add', methods=['POST'])
def upload_headportrait():
    file = request.files['file']
    user = current_user()
    if file and allowed_file(file.filename):
        # not consider the conditon filename is not secure 
        filename = secure_filename(file.filename)
        user_id = user.__dict__['id']
        filename = filename.rsplit('.', 1)[0] +  str(user_id) + '.' + filename.rsplit('.', 1)[1]
        file.save(os.path.join(upload_folder, filename))
    return redirect(url_for('.index', username=user.username))


@main.route('/headportrait/<int:u_id>')
def headportrait(u_id):
    file_list = os.listdir(upload_folder)
    for file in file_list:
        # do't forget turn to int 
        if u_id == int(file.rsplit('.', 1)[0][-1]):
            return send_from_directory(upload_folder, file)
    return abort(404)