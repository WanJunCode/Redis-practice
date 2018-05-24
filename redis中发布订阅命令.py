import redis
import time
import threading

r=redis.Redis('127.0.0.1','6379')

def publisher(n):
    time.sleep(1)
    for i in range(n):
        r.publish('channel',i)
        time.sleep(1)

def run_pubsub():
    threading.Thread(target=publisher,
                     args=(3,)).start()
    pubsub=r.pubsub()
    pubsub.subscribe(['channel'])
    count=0
    for item in pubsub.listen():
        print(item)
        count+=1
        if count==4:
            pubsub.unsubscribe()
        if count==5:
            break
run_pubsub()