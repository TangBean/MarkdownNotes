# 在 Django 中使用 Celery

参考：https://www.cnblogs.com/linxiyue/p/7518535.html

官方示例：https://github.com/celery/celery/tree/master/examples/django/

假设 Django 的目录组织如下：

```
- proj/
  - manage.py
  - proj/
    - __init__.py
    - settings.py
```

首先创建一个 `proj/proj/celery.py` 文件：

```python
from __future__ import absolute_import, unicode_literals
import sys
import os
from celery import Celery
import logging

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger('celery')
 
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

app = Celery('proj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix. This parameter is unnecessary.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
```

然后要保证 django 项目启动时上述的 app 被载入，修改 `proj/proj/__init__.py` 文件：

```python
from __future__ import absolute_import, unicode_literals
 
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app
 
__all__ = ['celery_app']
```

现在就可以在 INSTALLED_APPS 中的 app 下建立 tasks.py 文件了：

```
- app1/
    - tasks.py
    - models.py
- app2/
    - tasks.py
    - models.py
```

在 tasks.py 文件中可以这样写：

```python
# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

@shared_task
def add(x, y):
    return x + y

@shared_task
def mul(x, y):
    return x * y

@shared_task
def xsum(numbers):
    return sum(numbers)
```

然后在 views 中调用这些 tasks 中的函数即可异步运行。