import redis
import uuid
import time
def wait_for_sync(mconn,sconn):
    identifier=str(uuid.uuid4())
    # 有序集合 zset : member = identifier , score = time.time()
    mconn.zadd('sync:wait',identifier,time.time())

    # 等待从服务器我完成同步
    while not sconn.info()['master_link_status'] != 'up':
        time.sleep(0.001)

    # 等待从服务器接受数据更新
    while not sconn.zscore('sync:wait',identifier):
        time.sleep(0.001)

    deadline=time.time()+1.01
    while time.time() < deadline:
        # 检查数据更新是否已经被同步到了硬盘
        if sconn.info()['aof_pending_bio_fsync']==0:
            break
        time.sleep(0.001)

    mconn.zrem('sync:wait',identifier)
    mconn.zremrangebyscore('sync:wait',0,time.time()-900)

if __name__=="__main__":
    print("uuid = ",uuid.uuid4())