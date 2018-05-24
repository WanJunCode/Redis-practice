import redis
r=redis.Redis('127.0.0.1','6379')

pubsub=r.pubsub()
pubsub.subscribe(['channel'])
count=0
for item in pubsub.listen():
    print(item)
    count+=1
    # if count==4:
    #     pubsub.unsubscribe()
    # if count==5:
    #     break