#线程间通信

import time
import threading
from chapter11 import variables

from threading import Condition

#1. 生产者当生产10个url以后就就等待，保证detail_url_list中最多只有十个url
#2. 当url_list为空的时候，消费者就暂停

def get_detail_html(lock):
    #爬取文章详情页
    detail_url_list = variables.detail_url_list
    while True:

        if len(variables.detail_url_list):
            lock.acquire()
            if len(detail_url_list):
                url = detail_url_list.pop()
                lock.release()
                # for url in detail_url_list:
                print("get detail html started")
                time.sleep(2)
                print("get detail html end")
            else:
                lock.release()
                time.sleep(1)


def get_detail_url(lock):
    # 爬取文章列表页
    detail_url_list = variables.detail_url_list
    while True:
        print("get detail url started")
        time.sleep(4)
        for i in range(20):
            lock.acquire()
            if len(detail_url_list) >= 10:
                lock.release()
                time.sleep(1)
            else:
                detail_url_list.append("http://projectsedu.com/{id}".format(id=i))
                lock.release()
        print("get detail url end")


#1. 线程通信方式- 共享变量

if  __name__ == "__main__":
    lock = RLock()
    thread_detail_url = threading.Thread(target=get_detail_url, args=(lock,))
    for i in range(10):
        html_thread = threading.Thread(target=get_detail_html, args=(lock,))
        html_thread.start()
    # # thread2 = GetDetailUrl("get_detail_url")
    start_time = time.time()
    # thread_detail_url.start()
    # thread_detail_url1.start()
    #
    # thread1.join()
    # thread2.join()

    #当主线程退出的时候， 子线程kill掉
    print ("last time: {}".format(time.time()-start_time))