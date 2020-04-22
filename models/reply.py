from models import Mongo
from models.user import User
# from models.post import Post


class Reply(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('content', str, ''),
        ('post_id', int, -1),
        ('user_id', int, -1),
    ]

    def user(self):
        user = User.find_by(id=self.user_id)
        return user

    # def post(self):
    #     post = Post.find_by(id=self.post_id)
    #     return post