import redis
import time

def list_item(conn,itemid,sellerid,price):
    # inventory:17 用户包裹
    inventory = "inventory:%s" % (sellerid)
    item = "%s.%s" % (itemid, sellerid)
    # 设置时间限制
    end = time.time()+5
    pipe = conn.pipeline()

    while time.time() < end:
        try:
            # Redis Watch 命令用于监视一个(或多个) key ，
            # 如果在事务执行之前这个(或这些) key 被其他命令所改动，那么事务将被打断
            pipe.watch(inventory)
            if not pipe.sismember(inventory, itemid):
                pipe.unwatch()
                return None

            # 标记一个事务块的开始
            pipe.multi()
            # zset 有序字典
            pipe.zadd("market:", item, price)
            # set 字典
            pipe.srem(inventory, itemid)
            pipe.execute()
            return True
        except redis.exceptions.WatchError:
            pass
    return False