import redis

conn=redis.Redis('127.0.0.1','6379')

pipe=conn.pipeline()
pipe.hmset("users:17",{"name":"Frank","funds":43})
pipe.sadd("inventory:17","itemL","itemM","itemN")

pipe.hmset("users:27",{"name":"Bill","funds":125})
pipe.sadd("inventory:27","itemO","itemP","itemQ")

pipe.zadd("market:","itemA.4",35,"itemC.7",48,"itemE.2",60,"itemG.3",73)

pipe.execute()