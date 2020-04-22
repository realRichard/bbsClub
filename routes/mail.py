from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    abort,
)

from routes import current_user

from models.mail import Mail

from utils import log


main = Blueprint('mail', __name__)

@main.route('/')
def index():
    user = current_user()
    if user is not None:
        sent_mail = user.all_sent_mail()
        received_mail = user.all_received_mail()
        return render_template('/mail/mail.html', user=user, sent_mail=sent_mail, received_mail=received_mail)
    else:
        flash('要先登入才能发私信哦')
        return redirect(url_for('auth.index'))


@main.route('/send', methods=['POST'])
def send():
    form = request.form
    user = current_user()
    if user.is_receiver_existent(int(form.get('receiver_id'))):
        new_mail = Mail.new(form, sender_id=user.id)
        new_mail.hold()
    else:
        flash('没有此用户')
    return redirect(url_for('.index'))

@main.route('/detail')
def detail():
    m_id = request.args.get('id', None)
    if m_id is not None:
        m_id = int(m_id)
        mail = Mail.find_by(id=m_id)
        user = current_user()
        if mail is not None and (mail.sender_id == user.id or mail.receiver_id == user.id):
            if mail.receiver_id == user.id:
                mail.read()
            return render_template('/mail/detail.html', mail=mail, user=user)
    return abort(404)
