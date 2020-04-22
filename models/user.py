import hashlib

from utils import log
from config import salt

from models import (
    Mongo,
    Role,
)

from models.mail import Mail


class User(Mongo, Role):
    __fields__ = Mongo.__fields__ + [
        ('permissions', int, 1),
        ('username', str, ''),
        ('password', str, ''),
        ('signature', str, ''),
    ]

    @classmethod
    def validate_login(cls, form):
        username = form.get('username')
        password = form.get('password')
        u = cls.find_by(username=username)
        if u is None:
            return None
        elif u.__dict__['password'] == cls.salted_password(password):
            return u
        else:
            return None

    @classmethod
    def register(cls, form):
        username = form.get('username', '')
        password = form.get('password', '')
        if len(username) > 0 and User.find_by(username=username) is None:
            new_user = cls.new(form)
            new_user.password = cls.salted_password(password)
            new_user.hold()
            return new_user
        else:
            return None

    def is_administartor(self):
        return self.has_privilege('admin')

    def is_receiver_existent(self, receiver_id):
        user = self.find_by(id=receiver_id)
        if user is not None:
            return True
        else:
            return False

    def all_sent_mail(self):
        mails = Mail.find_all(sender_id=self.id)
        return mails

    def all_received_mail(self):
        mails = Mail.find_all(receiver_id=self.id)
        return mails

    @staticmethod
    def hashed_password(password):
        # encode to bytes object
        pwd = password.encode('ascii')
        p = hashlib.sha512(pwd)
        # get back digest str
        return p.hexdigest()

    @staticmethod
    def salted_password(password):
        def sha512(ascii_str):
            return hashlib.sha512(ascii_str.encode('ascii')).hexdigest()
        pwd1 = sha512(password)
        pwd2 = sha512(pwd1 + salt)
        return pwd2


