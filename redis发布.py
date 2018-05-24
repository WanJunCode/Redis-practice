import redis
import time
import threading

r=redis.Redis('127.0.0.1','6379')

while True:
    x=input()
    r.publish('channel',str(x))