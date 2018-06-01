import redis
import os
"""
用于处理新日志
path 表示日志文件路径
callback 用于处理每行操作的回调函数
"""

def process_logs(conn,path,callback):
    # 获取文件当前的处理进度 string
    current_file,offset=conn.mget('progress:file','progress:position')
    pipe = conn.pipeline()

    # 使用闭包 来减少重复代码
    def update_progress():
        # 更新正在处理的日志文件的名字和偏移量 string
        pipe.mset({
            'progress:file':fname,
            'progress:position':offset
        })
        pipe.execute()

    # 有序的遍历各个文件文件
    for fname in sorted(os.listdir(path)):
        # 判断该文件是否已经处理过
        if fname < current_file:
            continue

        inp = open(os.path.join(path,fname),'rb')
        if fname == current_file:
            inp.seek(int(offset,10))
        else:
            offset=0

        current_file=None

        # 枚举函数遍历一个由文件行组成的序列  行号lno  行数据line
        # enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。
        for lno,line in enumerate(inp):
            # 使用回调函数处理日志行
            callback(pipe,line)
            # 更新偏移量
            offset += int(offset)+len(line)

            # 每处理 1000 个日志行，更新一次文件
            if not (lno+1) % 1000:
                update_progress()
        update_progress()
        inp.close()
