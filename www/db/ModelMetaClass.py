import logging
from www.db.Field import Field

# 为生成的每个实体类,完成数据库字段到实体类属性的映射(ORM)
class ModelMetaClass(type):

    def __new__(cls, name, bases, attrs):
        # 排除Model类
        if name == 'Model':
            return type.__new__(cls,name,bases,attrs)

        # 如果不指定tableName,默认类名为tableName
        tableName = attrs.get('__table__') or name
        logging.info('find model : %s (table: %s)' % (name,tableName))

        # 属性和列的映射关系
        mappings = dict()
        # 除主键外的所有属性
        fields = []
        # 主键
        primaryKey = None

        # 只有是Field类型的才处理映射关系,Field代表的是数据库列的属性
        for k,v in attrs.items():
            if isinstance(v,Field):
                logging.info('find mapping : %s -> %s' %(k,v))
                mappings[k] = v
                # 如果该列是主键,返回True
                if v.primary_key:
                    # 判断是否已经存在了主键,这里没有考虑复合主键的情况
                    if primaryKey:
                        raise RuntimeError('Duplicate primary key for field: %s' % k)
                    primaryKey = k
                else:
                    fields.append(k)
        if not primaryKey:
            raise RuntimeError('primary key not found !')

        # 移除类的属性名,防止与实例的属性名冲突
        for k in mappings.keys():
            attrs.pop(k)

        # 为每一列加上``,防止字段名与mysql关键字冲突
        escaped_fields = list(map(lambda f : '`%s`' % f, fields))
        print(escaped_fields)

        # 为每个类添加以下方法,attrs表示类属性和方法的集合
        attrs['__mappings__'] = mappings
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey
        attrs['__fields__'] = fields

        # 构造CRUD sql语句
        select_sql = 'select `%s`,%s from %s' % (primaryKey, ','.join(escaped_fields), tableName)
        # insert_sql = 'insert into %s(`%s`,%s) values(%s)' % (primaryKey, tableName, ','.join(escaped_fields), ','.join(map(lambda f : '?', escaped_fields)))
        update_sql = 'update %s set %s where %s = ?' % (tableName, ','.join(map(lambda f : '`%s = ?`' % mappings.get(f).name, fields)), primaryKey)
        delete_sql = 'delete from %s where %s = ?' % (tableName, primaryKey)
        attrs['__select__'] = select_sql
        # attrs['__insert__'] = insert_sql
        attrs['__update__'] = update_sql
        attrs['__delete__'] = delete_sql

        return type.__new__(cls,name,bases,attrs)