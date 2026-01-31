import redis
import fastapi
import streamlit

print("libtaties working")

try:
    r = redis.Redis(host='localhost', port=6379)
    if r.ping():
        print("redis is connecte")
except:
    print("rdis connection failed")
