import redis
import time
import json

QUIT = False

# 调度缓存和终止缓存的函数
def schedule_row_cache(conn,row_id,delay):
    conn.zadd('delay:',row_id,delay)
    conn.zadd('schedule:',row_id,time.time())

# 缓存函数
def cache_rows(conn):
    while not QUIT:
        # 读取调度有序集合的第一个元素以及该元素的分值
        next = conn.zrange('schedule:',0,0,withscores=True)
        now = time.time()
        if not next or next[0][1] > now:
            # 如果next 不存在或者 时间戳所指定的时间尚未来临
            time.sleep(0.05)
            continue

        row_id=next[0][0]

        # 获得延迟时间
        delay = conn.zscore('delay:',row_id)
        if delay <= 0:
            conn.zrem('delay:',row_id)
            conn.zrem('schedule',row_id)
            # 删除该 商品 row_id 对应的 字符串
            conn.delete('inv:'+row_id)
            continue

        # 从数据库中读取数据行
        row = Inventory.get(row_id)
        # 重新调度时间并设置缓存值
        conn.zadd('schedule:',row_id,now+delay)
        conn.set('inv:'+row_id,json.dumps(row.to_dict()))