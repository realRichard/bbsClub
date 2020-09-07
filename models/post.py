import time
import json

from models import Mongo
from models.user import User
from models.reply import Reply
from models.board import Board
from models.cache import (
    MemoryCache,
    RedisCache,
)

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

    should_update_all = True
    # 1. memory cache
    # memory_cache = MemoryCache()
    # 2. redis cache
    redis_cache = RedisCache()

    def to_json(self):
        d = dict()
        for k in self.__class__.__fields__:
            key = k[0]
            if not key.startswith('_'):
                d[key] = getattr(self, key)
        return json.dumps(d)

    @classmethod
    def from_json(cls, j):
        d = json.loads(j)
        instance = cls()
        for k, v in d.items():
            setattr(instance, k, v)
        return instance

    @classmethod
    def all_delay(cls):
        # supposing this's a time consuming operating
        # time.sleep(3)
        return cls.all()

    def hold(self):
        super().hold()
        self.__class__.should_update_all = True

    @classmethod
    def cache_all(cls):
        # 1.memory cache
        # if cls.should_update_all is True:
        #     log('should_update_all')
        #     cls.memory_cache.set('post_all', cls.all_delay())
        #     cls.should_update_all = False
        # return cls.memory_cache.get('post_all')
        # 2. redis cache
        if cls.should_update_all:
            log('should_update_all')
            cls.redis_cache.set('post_all', json.dumps([cls.to_json(i) for i in cls.all_delay()]))
            cls.should_update_all = False
        j = json.loads(cls.redis_cache.get('post_all'))
        return [cls.from_json(i) for i in j]

    @classmethod
    def find_all(cls, **kwargs):
        for k, v in kwargs.items():
            key = k
            value = v
        posts = cls.cache_all()
        return [p for p in posts if getattr(p, key) == value]

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
