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





## logging 模块





## 函数





## 面向对象





## 多进程与多线程









