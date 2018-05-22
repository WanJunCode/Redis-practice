import redis

def cache_reuqest(conn,request,callback):
    if not can_cache(conn,request):
        return callback(request)

    # 将请求转换成一个简单的字符串键，方便以后进行查找
    page_key='cache:'+hash_request(request)
    # 尝试查找被缓存的页面
    content=conn.get(page_key)

    if not content:
        # 如果页面不存在，使用回调函数生成页面
        content=callback(request)
        # 将新生成的页面放到缓存里面去
        conn.setex(page_key,content,300)

    return content