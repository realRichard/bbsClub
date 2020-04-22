from models import Mongo


class Mail(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('title', str, ''),
        ('content', str, ''),
        ('check', bool, False),
        ('sender_id', int, -1),
        ('receiver_id', int, -1),
    ]

    def read(self):
        self.check = True
        self.hold()