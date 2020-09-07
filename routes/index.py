from flask import (
    Blueprint,
    render_template,
    request,
)

from models.post import Post
from models.board import Board
from models import Pagination

from utils import (
    log,
    find_all_and_separate,
)


main = Blueprint('index', __name__)

@main.route('/')
def index():
    boards = Board.all()
    # you can set the quantity of unreplied_post by list slicing
    unreplied_posts = [p for p in Post.cache_all() if len(p.replies()) == 0]
    board_name = request.args.get('tab', '全部')
    # current_page is str passed from url
    # page 1 by default
    current_page = int(request.args.get('page', 1))
    if board_name == '全部':
        # top_posts = Post.find_all(top=True)
        # ordinary_posts = Post.find_all(top=False)
        # for performance
        ordinary_posts = Post.cache_all()
        top_posts = find_all_and_separate(ordinary_posts, top=True)
        top_posts = sorted(top_posts, key=lambda post: post.ct, reverse=True)
        ordinary_posts = sorted(ordinary_posts, key=lambda post: post.ct, reverse=True)
        sorted_posts = top_posts + ordinary_posts
    else:
        board = Board.find_by(name=board_name)
        if board is not None:
            # posts = Post.find_all(board_id=board.id)
            # top_posts = [p for p in posts if p.top == True]
            # ordinary_posts = [p for p in posts if p.top == False]
            # for performance
            ordinary_posts = Post.find_all(board_id=board.id)
            top_posts = find_all_and_separate(ordinary_posts, top=True)
            top_posts = sorted(top_posts, key=lambda post: post.ct, reverse=True)
            ordinary_posts = sorted(ordinary_posts, key=lambda post: post.ct, reverse=True)
            sorted_posts = top_posts + ordinary_posts
            # print('sorted_posts', len(sorted_posts))
        else:
            # in order to keep the consistency down here
            # we give the sorted_posts empty list
            sorted_posts = []
    page = Pagination(len(sorted_posts), current_page)
    data = page.data_by_page(sorted_posts)
    return render_template('index.html', data=data, page=page, unreplied_posts=unreplied_posts, boards=boards)
