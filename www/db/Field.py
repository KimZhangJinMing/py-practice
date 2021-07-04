# Filed是对数据库的每一列的抽象
class Field(object):

    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s , %s, %s, %s， %s>' % (self.__class__.__name__, self.name, self.column_type, self.primary_key, self.default)


class StringField(Field):

    # 调用父类的方法不需要传入self
    def __init__(self, name=None, column_type='varchar(100)', primary_key=False, default=None):
        super().__init__(name, column_type, primary_key, default)


class IntField(Field):

    def __init__(self, name=None, column_type='int(11)', primary_key=False, default=None):
        super().__init__(name, column_type, primary_key, default)
