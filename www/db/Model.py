import logging
from www.db.Mysql import *
from www.db.ModelMetaClass import ModelMetaClass


class Model(dict,metaclass=ModelMetaClass):

    # 调用父类的__init__方法
    def __init__(self, **kw):
        super(Model,self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(r" 'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self,key):
        return getattr(self, key, None)

    def getValueOrDefault(self,key):
        value = self.getValue(self,key)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug("using default value for %s, %s" % (key, str(value)))
                setattr(self,key,value)
        return value

    @classmethod
    async def find(cls, primaryKey):
        print(cls.__select__)
        # 调用mysql的select进行查询,根据主键查找只能有一条数据,size写死为1
        rs = await select('%s where %s = ?' % (cls.__select__, cls.__primary_key__), primaryKey,1)
        print(rs)
        # if len(rs) == 0:
            # return None
        return cls(**rs[0])
