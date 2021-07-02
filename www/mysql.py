import aiomysql
import logging

logging.basicConfig(level=logging.info)
__pool

# 创建数据库连接池
async def create_pool(loop, **kw):
    logging.info("create db connection pool....")
    global __pool
    __pool =  await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw.get('user'),
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset','utf8'),
        autocommit=kw.get('autocommit',True),
        maxsize=kw.get('maxsize',10),
        minsize=kw.get('minsize',1),
        loop=loop
    )


async def select(sql,args, size=None):
    logging.info("select sql -->: %s" % sql)
    with await __pool as conn:
        cur = await conn.cursor()
        await cur.execute(sql.replace('?','%s'), args or ())
        if size:
            rs = await cur.fetchmany(size)
        else:
            rs = await cur.fetchall()
        await cur.close()
        logging.info("row return : %s" % len(rs))
        return rs


async def execute(sql, args):
    logging.info("execute sql -->: %s" % sql)
    with await __pool as conn:
        try:
            cur = await conn.cursor()
            await cur.execute(sql.replace('?', '%s'), args)
            # 通过rowcount返回结果数
            affected = cur.rowcount
            await cur.close()
        except BaseException:
            raise
        return affected



