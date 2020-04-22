import time
import math

from pymongo import MongoClient


mongo = MongoClient()


def next_id(name):
    query = {
        'name': name,
    }
    update = {
        '$inc': {
            'seq': 1,
        }
    }
    kwargs = {
        'query': query,
        'update': update,
        # 更新插入
        'upsert': True,
        'new': True,
    }
    # 存储数据的 id
    doc = mongo.bbs['data_id']
    new_id = doc.find_and_modify(**kwargs).get('seq')
    return new_id


class Mongo(object):
    __fields__ = [
        '_id',
        # (字段名, 类型, 值)
        ('id', int, -1),
        ('type', str, ''),
        ('deleted', bool, False),
        ('ct', int, 0),
        ('ut', int, 0),
    ]

    @classmethod
    def has(cls, **kwargs):
        return cls.find_one(**kwargs) is not None

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    @classmethod
    def new(cls, form=None, **kwargs):
        """
        new 是给外部使用的函数
        """
        name = cls.__name__
        # 创建一个空对象
        m = cls()
        # 把定义的数据写入空对象, 未定义的数据输出错误
        fields = cls.__fields__.copy()
        # 去掉 _id 这个特殊的字段
        fields.remove('_id')
        if form is None:
            form = {}

        for f in fields:
            k, t, v = f
            if k in form:
                setattr(m, k, t(form[k]))
            else:
                # 设置默认值
                setattr(m, k, v)
        # 处理额外的参数 kwargs
        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError
        # 写入默认数据
        m.id = next_id(name)
        ts = int(time.time())
        m.ct = ts
        m.ut = ts
        # m.deleted = False
        m.type = name.lower()
        m.hold()
        return m

    @classmethod
    def _new_with_bson(cls, bson):
        """
        这是给内部 all 这种函数使用的函数
        从 mongo 数据中恢复一个 model
        """
        m = cls()
        fields = cls.__fields__.copy()
        # 去掉 _id 这个特殊的字段
        fields.remove('_id')
        for f in fields:
            k, t, v = f
            if k in bson:
                setattr(m, k, t(bson[k]))
            else:
                # 设置默认值
                setattr(m, k, v)
        setattr(m, '_id', bson['_id'])
        # 这一句必不可少，否则 bson 生成一个新的 _id
        # FIXME, 因为现在的数据库里面未必有 type
        # 所以在这里强行加上
        # 以后洗掉 bbs 的数据后应该删掉这一句
        m.type = cls.__name__.lower()
        return m

    @classmethod
    def all(cls):
        # 按照 id 升序排序
        # name = cls.__name__
        # ds = mongua.bbs[name].find()
        # l = [cls._new_with_bson(d) for d in ds]
        # return l
        return cls._find()        

    @classmethod
    def _find(cls, **kwargs):
        """
        mongo 数据查询
        """
        name = cls.__name__
        # TODO 过滤掉被删除的元素
        # kwargs['deleted'] = False
        flag_sort = '__sort'
        sort = kwargs.pop(flag_sort, None)
        ds = mongo.bbs[name].find(kwargs)
        if sort is not None:
            ds = ds.sort(sort)
        l = [cls._new_with_bson(d) for d in ds]
        return l

    @classmethod
    def _find_raw(cls, **kwargs):
        name = cls.__name__
        # should be ds = mongo.bbs[name].find(kwargs)
        ds = mongo.bbs[name]._find(kwargs)
        l = [d for d in ds]
        return l
        # 直接 list() 就好了
        # return list(ds)

    @classmethod
    def _clean_field(cls, source, target):
        """
        清洗数据用的函数
        例如 User._clean_field('is_hidden', 'deleted')
        把 is_hidden 字段全部复制为 deleted 字段
        """
        ms = cls._find()
        for m in ms:
            v = getattr(m, source)
            setattr(m, target, v)
            m.hold()

    @classmethod
    def find_by(cls, **kwargs):
        return cls.find_one(**kwargs)

    @classmethod
    def find_all(cls, **kwargs):
        return cls._find(**kwargs)

    @classmethod
    def find(cls, id):
        return cls.find_one(id=id)
    
    @classmethod
    def get(cls, id):
        return cls.find_one(id=id)

    @classmethod
    def find_one(cls, **kwargs):
        # TODO 过滤掉被删除的元素
        # kwargs['deleted'] = False
        l = cls._find(**kwargs)
        if len(l) > 0:
            return l[0]
        else:
            return None

    @classmethod
    def upsert(cls, query_form, update_form, hard=False):
        ms = cls.find_one(**query_form)
        if ms is None:
            query_form.update(**update_form)
            ms = cls.new(query_form)
        else:
            ms.update(update_form, hard=hard)
        return ms

    def update(self, form, hard=False):
        for k, v in form.items():
            if hard or hasattr(self, k):
                setattr(self, k, v)
        # self.updated_time = int(time.time()) fixme
        self.hold()

    def hold(self):
        name = self.__class__.__name__
        mongo.bbs[name].save(self.__dict__)

    def delete(self):
        name = self.__class__.__name__
        query = {
            'id': self.id,
        }
        values = {
            'deleted': True,
        }
        mongo.bbs[name].update_one(query, values)

    def blacklist(self):
        b = [
            '_id',
        ]
        return b

    def json(self):
        _dict = self.__dict__
        d = {k: v for k, v in _dict.items() if k not in self.blacklist()}
        return d

    def data_count(self):
        name = self.__class__.__name__
        fk = '{}_id'.format(name.lower())
        query = {
            fk: self.id,
        }
        count = mongo.bbs[name].find(query).count()
        return count

    def format_ct(self):
        # ct = time.strftime("%Y-%m-%d %H:%M:%S", self.__dict__['ct'])
        # TypeError: Tuple or struct_time argument required
        # do't forget time.localtime(time.time()), localtime need timestamp paremeter
        ct = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.__dict__['ct']))
        return ct



class Role(object):
    privilege = {
        'ordinary': 1,
        'admin': 2,
    }

    def has_privilege(self, value):
        # via self.__class__ to access class attribute in instance method 
        return self.permissions & self.__class__.privilege.get(value) == self.__class__.privilege.get(value)

    def add_privilege(self, value):
        if not self.has_privilege(value):
            self.permissions += self.__class__.privilege.get(value)
            self.hold()

    def remove_privilege(self, value):
        if self.has_privilege(value):
            self.permissions -= self.__class__.privilege.get(value)
            self.hold()

    def reset_privilege(self):
        self.permissions = 1
        self.hold()


class Pagination(object):
    def __init__(self, length, current_page=1, per_page_max=10):
        self.per_page_max = per_page_max
        # 向上取整
        self.total_page = math.ceil(length / self.per_page_max)
        if current_page < 1:
            self.current_page = 1
        elif current_page > self.total_page:
            self.current_page = self.total_page
        else:
            self.current_page = current_page

    def data_by_page(self, data):
        p = (self.current_page - 1) * self.per_page_max
        return data[p:p + self.per_page_max]

    def previous_page(self):
        if self.current_page == 1:
            return None
        else:
            return self.current_page - 1

    def next_page(self):
        if self.current_page == self.total_page:
            return None
        else:
            return self.current_page + 1
