from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)

from models.user import User

from routes import current_user

from utils import log


main = Blueprint('auth', __name__)

@main.route('/')
def index():
    return render_template('/auth/registerLogin.html')


@main.route('/loginout', methods=['POST'])
def login_out():
    form = request.form
    user = current_user()
    user_id = form.get('id', None)
    if user_id is not None:
        user_id = int(user_id)
        if user.id == user_id:
            session.pop('user_id', None)
            return redirect(url_for('.index'))    
    flash('未成功退出')
    return redirect(url_for('user.index', username=user.username))


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    new_user = User.register(form)
    if new_user is  None:
        flash('未注册成功， 用户名不合法或已被注册')
    else:
        flash('注册成功, 尝试登入吧')
    return redirect(url_for('.index'))


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    user = User.validate_login(form)
    if user is None:
        flash('登入失败，用户名或密码不正确')
        return redirect(url_for('.index'))
    else:
        session['user_id'] = user.id
        session.permanent = True
        username = user.__dict__['username']
        return redirect(url_for('user.index', username=username))
