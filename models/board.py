from models import Mongo


class Board(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('name', str, ''),
    ]