import json

from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    abort,
)

from models.post import Post
from models.board import Board

from routes import current_user

from utils import log


main = Blueprint('post', __name__)

@main.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        user = current_user()
        if user is not None:
            form = request.form
            user_id = user.__dict__['id']
            # plus user_id on his post
            new_post = Post.new(form, user_id=user_id)
            new_post.hold()
            return redirect(url_for('.detail', id=new_post.id))
        else:
            flash('未登入， 不能发帖哦')
    boards = Board.all()
    return render_template('post/new.html', boards=boards)


@main.route('/delete', methods=['POST'])
def delete():
    post_id = request.args.get('id', None)
    user = current_user()
    if post_id is not None:
        post_id = int(post_id)
        post = Post.find_by(id=post_id)
        if post is not None and post.user_id == user.id:
            p = Post.delete(id=post_id)
            return json.dumps(p.__dict__, ensure_ascii=False)
    return redirect(url_for('user.index', username=user.username))


@main.route('/detail/<int:id>')
def detail(id):
    post = Post.find_by(id=id)
    if post is not None:
        post.auto_increment_views()
        replies = post.replies()
        return render_template('post/detail.html', post=post, replies=replies)
    else:
        return abort(404)