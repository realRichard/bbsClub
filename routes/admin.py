from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
)

from models.board import Board

from routes import current_user


main = Blueprint('admin', __name__)

@main.route('/board', methods=['GET', 'POST'])
def board():
    user = current_user()
    if user is not None and user.is_administartor():
        if request.method == 'POST':
            form = request.form
            new_board = Board.new(form)
            new_board.hold()
        boards = Board.all()
        return render_template('admin/board.html', boards=boards)
    else:
        return redirect(url_for('index.index'))
