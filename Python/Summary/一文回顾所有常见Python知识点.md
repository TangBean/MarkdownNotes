# 一文回顾所有常见 Python 知识点



## 正则表达式

模块：`import re`

### 常用函数

- `match(pattern, string, flags=0)`
	- 从 string 开头开始匹配，如果开头就不匹配会直接返回 None，
	- 匹配不成功会返回 None
	- 匹配成功会返回第一次匹配的对象
- `search(pattern, string, flags=0)`
	- 从 string 中匹配字符串，不一定必须从开头开始
	- 匹配不成功会返回 None
	- 匹配成功会返回第一次匹配的对象
- `findall(pattern, string, flags=0)`
	- 返回所有匹配结果，返回一个 List
- `sub(pattern, repl, string, count=0)`
	- 替换 string 中匹配的字符串为 repl
	- count 用来表示替换多少个
		- count == 0，替换所有匹配的字符为替换字符
		- count > 0，替换 count 个匹配的字符为替换字符
- `split(pattern, string, maxsplit)`
	- 根据 pattern 分割 string
	- maxsplit 表示最大
- `compile(pattern, flags=0)`
	- 编译正则表达式，返回一个 pattern 对象

### flags 标志位

flags 标志位用于设置匹配的附加选项，常用的 flags 如下：

| 选项   | 作用                                  |
| ------ | ------------------------------------- |
| `re.I` | 忽略大小写                            |
| `re.L` | 字符集本地化，用于多语言环境          |
| `re.M` | 多行匹配                              |
| `re.S` | 使用 `.` 匹配包括 `\n` 在内的所有字符 |
| `re.X` | 忽略正则表达式中的空白、换行          |

### 正则表达式

元字符是正则表达式中最基本的组成单位，一个正则表达式中至少要包含一个元字符。

元字符表是由一组地位平等的元字符组成，匹配时会选取表中的任意一个字符，元字符表由 `[]` 包起来，如 `[xyz]`。

如果需要对正则表达式进行嵌套，就需要使用分组 `()`，我们可以通过分组将一些小元字符组合成一个大元字符。

**Python 常用的元字符：**

| 元字符   | 作用                             | 元字符       | 作用                        |
| -------- | -------------------------------- | ------------ | --------------------------- |
| `^`      | 开始字符                         | `[m]`        | 匹配单个字符串              |
| `$`      | 结束字符                         | `[m-n]`      | 匹配 m ~ n 之间的字符       |
| `\w`     | 匹配字母、数组、下划线           | `m|m2..n|n2` | 匹配多个字符串              |
| `\W`     | 匹配不是字母、数组、下划线的字符 | `[^m]`       | 匹配除 m 以外的字符串       |
| `\s`     | 匹配空白字符                     | `()`         | 分组                        |
| `\S`     | 匹配不是空白字符的字符           | `{m}`        | 重复 m 次                   |
| `\d`     | 匹配数字                         | `{m,n}`      | 重复 m ~ n 次               |
| `\D`     | 匹配不是数字的字符               | `*`          | 匹配 0 次或多次             |
| `\b`     | 匹配单词的开始和结束的位置       | `+`          | 匹配 1 次或多次             |
| `\B`     | 匹配不是单词的开始和结束的位置   | `?`          | p匹配 0 次或 1 次           |
| `.`      | 匹配任意字符                     | `*?`         | 匹配 0 次或多次，且最短匹配 |
| `{m,n}?` | 重复 m ~ n 次，且最短匹配        | `+?`         | 匹配 1 次或多次，且最短匹配 |
| `??`     | 匹配 0 次或 1 次，，且最短匹配   | `(?P<name>)` | 为分组命名，name为分组名    |
| `m|n`    | 匹配 m 或 n                      | `(?P=name)`  | 使用名为 name 的分组        |

### Example

```python
import re

string = 'hellomypythonhistorypythonourpythonend'
patt = '.python.'
patt = re.compile(patt)  # 预编译，用于之后对其进行复用
"""
看了一下源码，re 模块中有一个 cache，用来保存编译过的匹配模式。
这个 cache 有一个最大的大小限制：512，如果超过 512 就会执行 cache.clear()

不过呢，正是因为有 512 这个长度限制，所以如果后面可能会用很多次的匹配模式还是 compile 一下好一些！
"""

# 两个函数的共同点，都是返回匹配对象，并且只返回第一次匹配的对象
r1 = re.match(patt, string)  # 从头开始匹配，头不符合就返回 None
r2 = re.search(patt, string)  # 匹配整个字符串，字符串中有匹配的就可以

print(r1)  # None
print(r2)  # <_sre.SRE_Match object; span=(6, 14), match='ypythonh'>
print(r2.span())  # (6, 14)
print(r2.group())  # ypythonh


r3 = re.findall(patt, string)  # 返回所有匹配结果，返回的是一个 List
print(r3)  # ['ypythonh', 'ypythono', 'rpythone']


r4_1 = re.sub(patt, '$$$$', string, count=0)  # count == 0，会替换所有匹配的结果
r4_2 = re.sub(patt, '$$$$', string, count=2)  # 替换 2 个

print(r4_1)  # hellom$$$$istor$$$$u$$$$nd
print(r4_2)  # hellom$$$$istor$$$$urpythonend
```



## import 模块





## 解析 JSON

### 基本使用

```python
import json

'''
Python object -> JSON string: json.dumps()
JSON string -> Python object: json.loads()
如果是文件就用：json.dump() & json.load()
'''

python_obj = [{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}]
json_str = '{"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}'

json_str_change = json.dumps(python_obj, indent=4)
print(json_str_change)
''' 输出
[
    {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": 4,
        "e": 5
    }
]
'''

python_obj_change = json.loads(json_str)
print(type(python_obj_change))  # <class 'dict'>
print(python_obj_change['b'])  # 2
print(python_obj_change)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}

```

### Python to JSON 对照表

| JSON 类型        | Python 类型 |
| ---------------- | ----------- |
| Dict             | object      |
| list，tuple      | array       |
| string，unicode  | string      |
| int，long，float | number      |
| True             | true        |
| False            | false       |
| None             | null        |

### JSON to Python 对照表

| Python 类型 | JSON 类型 |
| ----------- | --------- |
| object      | dict      |
| array       | list      |
| string      | unicode   |
| int         | int，long |
| true        | True      |
| false       | False     |
| null        | None      |



## logging 模块

```python
import logging

logging.debug('debug message')
logging.info('info message')
logging.warn('warn message')
logging.error('warn message')
logging.critical('critical message')

'''
输出：日志级别 >= WARNING 才会输出，默认输出到 stdout
WARNING:root:warn message
ERROR:root:warn message
CRITICAL:root:critical message
'''
```



## 函数

### 关于 return

首先，Python 的函数是肯定有返回的，如果你没在函数中写 return，它会返回 None 的。

```python
def no_return_function():
    a = 1

res = no_return_function()
print(res)  # None
```

### 关于入参

#### Python 函数的 5 种类型参数

- **必选参数（位置参数）**

	- `def power(x, n):` 这种，调用的时候必须按照顺序传入 `x` 和 `n`

- **默认参数**

	- `def power(x, n=2):`，其中 `n` 就是一个默认参数
	- 默认参数必须指向一个不可变对象，比如可以是一个 tuple，但不能是一个 list

- **可变参数**

	- `def calc(*numbers):`，加了 `*` 的变量名会存放所有未命名的变量参数
	- 可变参数允许传入 0 个或任意个参数，这些可变参数在函数调用时会自动组装为一个 tuple
	- 如果想把一个 list `nums = [1, 2, 3]` 中的元素作为可变参数传入函数，可以这样写：`calc(*nums)`

- **关键字参数**

	- `def person(name, age, **kw):`，加了 `**` 的变量就是关键字参数

	- 关键字参数允许你传入 0 个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个 dict

	- 和可变参数类似，可以先组装出一个 dict，然后，把该 dict 转换为关键字参数传进去：

		```python
		extra = {'city': 'Beijing', 'job': 'Engineer'}
		person('Jack', 24, **extra)
		```

	- `**extra` 表示把 `extra` 这个 dict 的所有 key-value 用关键字参数传入到函数的 `**kw` 参数，`kw` 将获得一个 dict，注意 `kw` 获得的 dict 是 `extra` 的一份拷贝，对 `kw` 的改动不会影响到函数外的 `extra`

- **命名关键字参数**

	- 命名关键字参数需要一个特殊分隔符 `*`，`*` 后面的参数被视为命名关键字参数，就是说，必须有，必须传：

		```python
		def person(name, age, *, city, job):  # city, job 是命名参数，
		    print(name, age, city, job)
		```

	- 如果函数定义中已经有了一个可变参数，后面跟着的命名关键字参数就不再需要一个特殊分隔符 `*` 了：

		```python
		def person(name, age, *args, city, job):
		    print(name, age, args, city, job)
		```

	- 命名关键字参数可以有缺省值，从而简化调用：

		```python
		def person(name, age, *, city='Beijing', job):
		    print(name, age, city, job)
		```

	- 使用命名关键字参数时，要特别注意，如果没有可变参数，就必须加一个 `*` 作为特殊分隔符。如果缺少 `*`，Python 解释器将无法识别位置参数和命名关键字参数

#### `*args, **kwargs` 参数

```python
def func(*args, **kwargs)  # 传啥进去都行
func(*args, **kwargs)  # 任意函数，都可以通过类似 func(*args, **kw) 的形式调用
```

### 内部函数和闭包

- **相同点：**
	- 都是函数里面嵌套着函数的
- **不同点：**
	- 内部函数返回内部函数的直接调用
	- 闭包返回内部函数本身

```python
# 内部函数
def test(*args):
    def add(*args):
        return args
    return add(*args)  # 返回内部函数的直接调用

# 闭包
def greeting_conf(prefix):
    def greeting(name):
        print(prefix, name)
    return greeting  # 返回内部函数本身，就像是获取了一个装饰后的函数
```

### lambda 函数

#### 语法

```python
lambda var1, var2: expression

# e.g.
sum = lambda x, y: x + y
sum(1, 2)  # 调用
```

lambda 函数只会使代码更加简洁，并不会提高程序的运行效率。

lambda 函数经常用于 **Python 的函数式编程**，即 **允许把函数本身作为参数传入到另一个函数，还允许返回一个函数**。

#### 应用

**map() 函数：** `map` 将传入的函数依次作用到序列的每个元素，并把结果作为新的 `Iterator` 返回

map() 函数的语法：`map(函数, 序列)`

```python
squares = map(lambda x: x*x, [1,2,3,4,5,6,7,8,9])
```

**reduce() 函数：** `reduce` 把结果继续和序列的下一个元素做累积计算

reduce() 函数的语法：`reduce(函数, 序列)`

```python
# reduce 很适合用来实现阶乘
res = reduce(lambda x,y: x*y, [1,2,3,4,5,6,7,8,9])
```

### 列表生成式和生成器

**列表生成式：**

```python
>>> [x * x for x in range(1, 11)]
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

**生成器：** 把列表生成式的 `[]` 换成 `()` 就变成了一个生成器

```python
g = (x * x for x in range(10))
# g 是一个生成器对象，可以通过 next(g) 调用，如果没有元素了就会抛出 StopIteration 异常
# 不过这种调用方法太费劲了，比较优雅的做法是使用 for 循环
# 使用 for 循环后，我们就无需自己解决 StopIteration 的问题了
for n in g:
    print(n)
```

### 处理命令行参数

模块：`import getopt`

用到的时候再写……



## 面向对象





## 多进程与多线程









