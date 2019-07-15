# Celery 简单文档

官方文档：http://docs.celeryproject.org/en/latest/index.html

Celery 是一个由 Python 编写的简单、灵活、可靠的用来处理大量信息的分布式系统，它提供了操作和维护分布式系统所需的工具。**我们可以通过 Celery 提供的接口快速实现并管理一个分布式的任务队列。**

首先，我们需要明确，Celery 并不提供任务队列，它只是一个管理分布式任务队列的工具，也就是说，它提供了各种操作任务队列的接口，我们把任务队列给它，它就可以帮我们操作任务队列。

先来看几个 Celery 中的基本概念。

## 基本概念

### Brokers

Brokers 是经纪人、中间人的意思，在 Celery 中，Brokers 指的是任务队列，Celery 扮演生产者和消费者的角色，brokers 就是生产者和消费者存放 / 拿取任务的地方。

常见的 brokers 有 rabbitmq、redis、Zookeeper 等。

### Result Stores / backend

Result Stores 结果储存的地方，队列中的任务运行完后，需要让任务的提交者知道任务的结果或者任务的状态，那么就需要一个地方储存这些结果，这个地方就是 Result Stores。

常见的 Result Stores / backend 有 redis、Memcached 甚至常用的数据库都可以。

### Workers

Celery 中的工作者，类似于生产 / 消费模型中的消费者，它会从队列中取出任务并执行。

### Tasks

躺在 Brokers 中的任务，它会由任务提交者塞入任务队列，然被 workers 取出来拿去执行。

## 简单使用

要想用，先装包：

```shell
apt-get install redis-server
pip install redis
pip install celery
```

先写一个 Task：

```python
# tasks.py
from celery import Celery

# 配置好 celery 的 backend 和 broker
app = Celery('tasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0') 
 
@app.task  # 普通函数装饰为 celery task
def add(x, y):
    return x + y
```

接下来在 task.py 所在的目录运行：

```shell
celery -A tasks worker --loglevel=info
```

这个命令的作用是让去 tasks 任务集合取任务的 workers 们开始工作，不过此时 broker 中还没有任务，所以 workers 应该处于待命状态。

最后一步，把任务塞进任务队列，塞进去的方法就是调用我们之前写的那个被装饰成 Task 的函数啦。

```python
# trigger.py
from tasks import add
result = add.delay(4, 4) # 不能直接 add(4, 4)，这里需要用 celery 提供的接口 delay 进行调用
while not result.ready()
    time.sleep(1)
print 'task done: {0}'.format(result.get())
```

delay 返回的是一个 AsyncResult 对象，里面存的就是一个异步的结果，当任务完成时`result.ready()` 为 true，然后用 `result.get()` 取结果即可。（和 Java 里的 Future 对象差不多）

注意 `result.get()` 是一个阻塞方法，如果结果没有准备好，就会阻塞等待。

## 进阶使用

上面的使用方法过于简单了，并且定制话功能也不是很强，所以现在来看高级用法。

### 自定义 Task 类

除了官方提供给我们的 Task 类，我们也可以通过继承 Task 来实现自定义的 Task 修饰函数 add：

```python
# tasks.py
class MyTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        print 'task done: {0}'.format(retval)
        return super(MyTask, self).on_success(retval, task_id, args, kwargs)
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print 'task fail, reason: {0}'.format(exc)
        return super(MyTask, self).on_failure(exc, task_id, args, kwargs, einfo)
 
@app.task(base=MyTask)
def add(x, y):
    return x + y
```

而后相同的方式启动 workers：`celery -A tasks worker --loglevel=info`。

此时任务执行成功或失败后会执行我们自定义的 `on_failure ` 和 `on_success` 方法。（比如可以在 `on_failure ` 方法里打个 log 发个报警啥的）

### 绑定 Task 对象

让被修饰的函数成为 Task 对象的绑定方法，这样就相当于被修饰的函数成了 Task 的实例方法，可以调用 self 获取当前 task 实例的很多状态及属性。

使用方法：

```python
# tasks.py
from celery.utils.log import get_task_logger
 
logger = get_task_logger(__name__)
@app.task(bind=True)  # 这里加个 bind=True 就 OK
def add(self, x, y):
    logger.info(self.request.__dict__)
    return x + y
```

这样，执行中的任务可以通过 self 获取自己正在执行的任务的各种信息，它可以根据这些信息做很多其他操作，例如判断链式任务是否到结尾等。

### 获取任务执行状态

Celery 内置任务状态有如下几种：

| 参数    | 解释         |
| ------- | ------------ |
| PENDING | 任务等待中   |
| STARTED | 任务已开始   |
| SUCCESS | 任务执行成功 |
| FAILURE | 任务执行失败 |
| RETRY   | 任务将被重试 |
| REVOKED | 任务取消     |

例如我们要用 Celery 执行一个时间比较长的任务，如果无法获取任务的实时执行状态，我们肯定会等的不耐烦并且怀疑任务执行出错，一般我们会在 task 中设置一个任务执行状态来说明进度，并手动更新它，从而告诉回调当前任务的进度。

具体实现如下：

```python
# tasks.py
from celery import Celery
import time
 
@app.task(bind=True)
def test_mes(self):
    for i in xrange(1, 11):
        time.sleep(0.1)
        self.update_state(state="PROGRESS", meta={'p': i*10})  # 任务执行状态: state
    return 'finish'
```

```python
# trigger.py
from task import add,test_mes
import sys
 
def pm(body):
    res = body.get('result')
    if body.get('status') == 'PROGRESS':
        sys.stdout.write('\r任务进度: {0}%'.format(res.get('p')))
        sys.stdout.flush()
    else:
        print '\r'
        print res
r = test_mes.delay()
print r.get(on_message=pm, propagate=False)
```

### 定时/周期任务

设置周期任务需要以下两步：

- 在配置中配置好周期任务
- 运行一个周期任务触发器（celery-beat）

首先看配置部分：

```python
# celery_config.py
from datetime import timedelta
from celery.schedules import crontab

CELERY_TIMEZONE = 'UTC'

CELERYBEAT_SCHEDULE = {
    'ptask': {
        'task': 'tasks.period_task',
        'schedule': crontab(minute='30', hour='3', day_of_week=6)
    },
}
```

然后在 tasks.py 中增加要被周期执行的任务：

```python
# tasks.py
app = Celery('tasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')
app.config_from_object('celery_config')
 
@app.task(bind=True)
def period_task(self):
    print 'period task done: {0}'.format(self.request.id)
```

然后运行：

```shell
celery -A tasks worker --loglevel=info
celery -A task beat
```

周期任务就会正常执行啦！

### 链式任务

有些任务可能需由几个子任务组成，此时调用各个子任务的方式就变的很重要，尽量不要以同步阻塞的方式调用子任务，而是用异步回调的方式进行链式任务的调用。

**错误示例：**

```python
@app.task
def update_page_info(url):
    page = fetch_page.delay(url).get()  # 同步阻塞调用链
    info = parse_page.delay(url, page).get()
    store_page_info.delay(url, info)
 
@app.task
def fetch_page(url):
    return myhttplib.get(url)
 
@app.task
def parse_page(url, page):
    return myparser.parse_document(page)
 
@app.task
def store_page_info(url, info):
    return PageInfo.objects.create(url, info)
```

**正确示例 1：**

```python
def update_page_info(url):
    # fetch_page -> parse_page -> store_page
    chain = fetch_page.s(url) | parse_page.s() | store_page_info.s(url)
    chain()
 
@app.task()
def fetch_page(url):
    return myhttplib.get(url)
 
@app.task()
def parse_page(page):
    return myparser.parse_document(page)
 
@app.task(ignore_result=True)
def store_page_info(info, url):
    PageInfo.objects.create(url=url, info=info)
```

**正确示例 2:**

```python
fetch_page.apply_async((url), link=[parse_page.s(), store_page_info.s(url)])
```

链式任务中前一个任务的返回值默认是下一个任务的输入值之一（不想让返回值做默认参数可以用 `si()` 或者 `s(immutable=True)` 的方式调用）。

这里的 `s()` 是方法 `celery.signature()` 的快捷调用方式，signature 具体作用就是生成一个包含调用任务及其调用参数与其他信息的对象。类似偏函数的概念：先不执行任务，而是把任务与任务参数存起来以供其他地方调用。

