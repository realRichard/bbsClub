from models import Mongo
from models.user import User
from models.reply import Reply
from models.board import Board

from utils import log


class Post(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('title', str, ''),
        ('content', str, ''),
        ('views', int, 0),
        ('user_id', int, -1),
        ('board_id', int, -1),
        ('top', bool, False),
    ]

    def user(self):
        user = User.find_by(id=self.user_id)
        return user

    def board(self):
        board = Board.find_by(id=self.board_id)
        return board

    def auto_increment_views(self):
        self.__dict__['views'] += 1
        self.hold()

    def replies(self):
        r = Reply.find_all(post_id=self.id)
        return r
