# Pyspider实现知乎热搜的爬取

这篇笔记记录了使用 Pyspider 爬取知乎热搜问题的过程。



## Pyspider的安装及常用命令

```bash
pip install pyspider            # 安装pyspider
pip list                        # 列出所有已安装的包及其版本
pip list --outdate              # 列出所有过时的包
pip install --upgrade Jinja2    # 更新某个软件包
pyspider -c conf.json           # 启动pyspider
```



## CSS选择器

我们可以通过 PyQuery 来实现对响应页面指定元素的高效查询，这主要用到了一个叫 CSS 选择器的东西，CSS 选择器的具体的语法可以参考：[CSS 选择器参考手册](http://www.w3school.com.cn/cssref/css_selectors.ASP)。下面我们会简单的介绍一些简单的语法：

| **选择器**           | **描述**                                                     |
| -------------------- | ------------------------------------------------------------ |
| ``.class`            | `class="class"`                                              |
| ``#id`               | `<p id="id">`                                                |
| `div.inner`          | `<div class="inner">`                                        |
| `a[href^="http://"]` | 带 http 开头的 href 的 a 元素                                |
| `p div`              | p 元素下的 div 元素，不一定必须是父子关系，只要 div 是 p 的后代就行 |
| `p>div>span`         | p 元素下的 div 元素下的 span，必须是父子关系                 |
| `[target=_blank]`    | `Target=_blank`                                              |



## MySQLdb

### insert 操作

```python
def add_question(self, title, content, comment_count):
    try:
        cursor = self.conn.cursor();  # 获取光标，相当于 statement
        sql = "insert into question (title, content, user_id, created_date, comment_count) " \
        	  "values('%s', '%s', %d, %s, %d);" % (title, content, random.randint(1, 10), \
			 'now()', comment_count)
        cursor.execute(sql)  # 执行 sql 语句
        qid = cursor.lastrowid
        self.conn.commit()
        return qid
    except Exception as e:
        print(e)
        self.conn.rollback()
```

### select 操作

```python
def user_exist(self, username):
    try:
        cursor = self.conn.cursor()
        sql = "select id from user where name='%s';" % (username)
        cursor.execute(sql)
        res = cursor.fetchone()
        self.conn.commit()
        if res is None:
            return -1
        else:
            return res[0]
    except Exception as e:
        print(e)
        self.conn.rollback()
```



## 爬取知乎热搜

### Pyspider 的程序结构

我们首先先来介绍一下 Pyspider 的程序结构：

```python
class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            # 可以在这里配置一些响应头的操作
        }
    }

    def __init__(self):
        # 可以在这里进行一些初始化操作，如初始化数据库连接池，设置 cookie 信息等

    @every(minutes=24 * 60) # 每天执行一次
    def on_start(self):
        # crawl(要爬取的url, 
        # callback=爬取页面后调用哪个函数处理页面, 
        # cookies=请求时cookie的设置，我们要通过设置 cookie 中的 ticket 来让服务器以为我们已经登录了
        # validate_cert=False：处理https问题)
        self.crawl('https://www.zhihu.com/hot', 
                   callback=self.question_page, 
                   cookies=self.cookies, 
                   validate_cert=False)

    @config(age=10 * 24 * 60 * 60) # 在10天以内爬过的页面就不爬了
    def question_page(self, response):
        # save=我们想传给调用函数的参数，可以在 callback 函数中通过 response.save 来调用
        self.crawl(answer_url, 
                   callback=self.detail_page, 
                   params=self.form_data, 
                   validate_cert=False, 
                   save=save_param)

    # 最后，我们经过前面的各种页面跳转，终于到达了有我们想爬的数据的页面，我们要从这个页面中提取我们想要的数据
    @config(priority=2)
    def detail_page(self, response):
        data_obj = json.loads(response.content.decode('utf8')) # 解析 json 对象格式的数据
        # 各种处理
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
```

### 把自己伪装成 Google 爬虫

在 crawl_config 中设置 headers 为：

```python
crawl_config = {
    'headers': {
        'User-Agent': 'GoogleBot',
        'Host': 'www.zhihu.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
}
```

### 设置 cookie 来伪装登录

先登录知乎，登录知乎后按 F12 调出开发者页面，然后把里面的 cookie 值都复制出来，放到`__init__`函数中，用于之后请求页面时调用。

### 处理知乎问题页的 Ajax 翻页问题

知乎的问题页采用的是 Ajax 翻页，而且还不是那种一页看完之后，点击下一页它才刷新下一页的那种，而是通过滚动到最后之后，它会自动请求服务器发新的页面来那种。

通过观察知乎问题详情页的请求我发现，知乎请求新的页面用的不是 post 请求，而是一个 get 请求：

```python
"https://www.zhihu.com/api/v4/questions/" + str(qid) + "/answers"
```

这个 get 请求有如下几个参数：

```python
self.include_param = 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics'
self.form_data = {
    'include': self.include_param,
    'offset': '0',
    'limit': '10',
    'sort_by': 'default',
    'platform': 'desktop'
}
```

这个请求会返回 json 格式的数据，并且！我们完全不用自己去翻页，我们想要多少个问题的回答，就可以通过 offset 和 limit 来设置，还可以通过 sort_by 参数来选择排序方式！

之后我们只需要对得到的 json 数据进行处理就可以啦！json 字符串可以通过 python json 库的 load 函数来转成字典格式：

```python
data_obj = json.loads(response.content.decode('utf8'))
```

然后我们看看这个 json 串的格式，从里面取出来我们想要的数据就可以了！

详细实现：[zhihu_hot.py](./zhihu_hot.py).

