# ajax



## ajax 概述

ajax (asynchronous javascript and xml)，异步的 js 和 xml，它有如下功能：

- 能使用 js 访问服务器，而且是异步访问
- 服务器给客户端的响应一般是整个页面，但在 ajax 中是局部刷新，服务器不用再响应整个页面，只相应数据就行，响应的数据有如下格式：text，xml，json

### 异步交互和同步交互

**同步：**

- 发一个请求，就要等待服务器的响应结束，然后才能发第二个请求，中间只能卡着
- 刷新的是整个页面

**异步：**

- 发一个请求后，无需等待服务器的响应，然后就可以发第二个请求
- 可以使用 js 接收服务器的响应，然后使用 js 来局部刷新

### ajax 应用

- 百度的搜索框
- 用户注册时 (校验用户名是否被注册过)

### ajax 优缺点

**优点：**

- 异步交互：增强了用户的体验
- 因为服务器无需再响应整个页面，只需要响应部份内容，所以服务器的压力减轻了

**缺点：**

- ajax 不能应用在所有场景
- ajax 无端的增多了对服务器的访问次数，给服务器带来了压力 (好矛盾……)



## ajax 发送异步请求 (4步)

### 第一步：得到 XMLHttpRequest

得到 XMLHttpRequest 的方法：

- `var xmlHttp = new XMLHttpRequest();`
- `var xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");`
- `var xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");`

**示例：**

```javascript
function createXMLHttpRequest() {
    try {
        return new XMLHttpRequest();
    } catch(e) {
        try {
            return new ActiveXObject("Msxml2.XMLHTTP");
        } catch(e) {
            try {
                return new ActiveXObject("Microsoft.XMLHTTP");
            } catch(e) {
                alert("未知浏览器");
                throw e;
            }
        }
    }
}
```

### 第二步：打开与服务器的连接

`xmlHttp.open()`：用来打开与服务器的连接，需要三个参数：

- 请求方式：可以是 GET 或 POST
- 请求的 URL：指定服务器端资源，例如：/day23_1/AServlet
- 请求是否为异步：如果为 true 表示发送异步请求，否则同步请求

**示例：**`xmlHttp.open("GET", "/day23_1/AServlet", true);`

### 第三步：发送请求

`xmlHttp.send(null)`：参数就是请求体内容，如果是 GET 请求，必须给出 null

### 第四步：响应请求

- 想要知道请求被响应了，需要在 xmlHttp 对象的一个事件上注册监听器：onreadystatechange
- xmlHttp 可能返回如下 5 种状态：
  - 0 状态：刚创建，还没有调用 open() 方法 (第一步执行完的状态)
  - 1 状态：请求开始：调用了open() 方法，但还没有调用 send() 方法 (第二步执行完的状态)
  - 2 状态：调用完了send() 方法了 (第三步执行完的状态)
  - 3 状态：服务器已经开始响应，但不表示响应结束了！
  - 4 状态：服务器响应结束 (我们最关心的状态)
- 得到 xmlHttp 对象的状态：`var state = xmlHttp.readyState;`
- 得到服务器响应的状态码：`var status = xmlHttp.status;`
- 得到服务器响应的内容
    - `var content = xmlHttp.responseText;`：文本格式
    - `var content = xmlHttp.responseXML;`：xml 响应内容，就是 Document 对象啦

**示例：**

```javascript
xmlHttp.onreadystatechange = function() {  // xmlHttp的5种状态都会调用本方法
    if(xmlHttp.readyState == 4 && xmlHttp.status == 200) {  // 判断是否为4状态，而且还要判断状态码是否为200
        // 获取服务器的响应内容
        var text = xmlHttp.responseText;
    }
};
```

## 案例

### 案例一：发送 GET & POST 请求

如果发送请求时带有参数，一般用 POST 方法。

要在第二步与第三步之间加一个添加请求头操作：

```javascript
xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
```

**代码：**

ajax1.jsp

```html
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
<title>Title</title>
<script type="text/javascript">
    function createXMLHttpRequest() {
        try {
            return new XMLHttpRequest();
        } catch (e) {
            try {
                return ActiveXObject("Msxml2.XMLHTTP");
            } catch (e) {
                try {
                    return ActiveXObject("Microsoft.XMLHTTP");
                } catch (e) {
                    alert("未知浏览器");
                    throw e;
                }
            }
        }
    }
 
    window.onload = function () {
        var gbtn = document.getElementById("gbtn");
        var pbtn = document.getElementById("pbtn");
 
        gbtn.onclick = function () {
            var xmlHttp = createXMLHttpRequest();
            xmlHttp.open("GET", "<c:url value='/AServlet'/> ", true);
            xmlHttp.send(null);
            xmlHttp.onreadystatechange = function () {
                if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                    var text = xmlHttp.responseText;
                    var gh1 = document.getElementById("gh1")
                    gh1.innerText = text;
                }
            }
        }
 
        pbtn.onclick = function () {
            var xmlHttp = createXMLHttpRequest();
            xmlHttp.open("POST", "<c:url value="/AServlet"/> ", true);
            xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xmlHttp.send("username=张三")
            xmlHttp.onreadystatechange = function () {
                if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                    var text = xmlHttp.responseText;
                    var ph1 = document.getElementById("ph1");
                    ph1.innerText = text;
                }
            }
        }
    }
</script>
</head>
<body>
    <button id="gbtn">发送GET</button><br/>
    <h1 id="gh1"></h1><br/>
    <button id="pbtn">发送POST</button><br/>
    <h1 id="ph1"></h1>
</body>
</html>
```

Servlet：

```java
@WebServlet(name = "AServlet", urlPatterns = {"/AServlet"})
public class AServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
        throws ServletException, IOException {
        request.setCharacterEncoding("utf-8");
        response.setContentType("text/html;charset=utf-8");
        String username = request.getParameter("username");
        System.out.println(username + "发送了POST请求...");
        response.getWriter().println(username + "发送了POST请求...");
    }
 
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        request.setCharacterEncoding("utf-8");
        response.setContentType("text/html;charset=utf-8");
        System.out.println("Get Request");
        response.getWriter().println("Get Request");
    }
}
```

### 案例二：用户名是否被注册

```html
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
<title>Title</title>
<script type="text/javascript">
    function createXMLHttpRequest() {
        try {
            return new XMLHttpRequest();
        } catch (e) {
            try {
                return ActiveXObject("Msxml2.XMLHTTP");
            } catch (e) {
                try {
                    return ActiveXObject("Microsoft.XMLHTTP");
                } catch (e) {
                    alert("未知浏览器");
                    throw e;
                }
            }
        }
    }
 
    window.onload = function () {
        var usernameEle = document.getElementById("usernameEle");
        usernameEle.onblur = function () {
            var xmlHttp = createXMLHttpRequest();
            xmlHttp.open("POST", "<c:url value='/BServlet'/> ", true);
            xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xmlHttp.send("username=" + usernameEle.value);
            xmlHttp.onreadystatechange = function () {
                if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                    var state = xmlHttp.responseText;
                    var errorSpanEle = document.getElementById("errorSpan");
                    if (state == "0") {
                        errorSpanEle.innerText = "用户名已被注册";
                    } else {
                        errorSpanEle.innerText = "";
                    }
                }
            }
        }
    }
</script>
</head>
<body>
<form action="" method="post">
    Username:<input type="text" name="username" id="usernameEle" /><span id="errorSpan"></span><br/>
    Password:<input type="password" name="password" id="passwordEle" /><br/>
    <input type="submit" value="Submit"/>
</form>
</body>
</html>
```

### 案例三：响应内容为xml

- 服务器端：
    - 设置响应头：`response.setContentType("text/xml;charset=utf-8")`
- 客户端：
    - 获取 XML 数据：`var doc = xmlHttp.responseXML;`

### 案例四：省市联动

city.jsp

```html
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
<title>Title</title>
<script type="text/javascript">
    function createXMLHttpRequest() {
        try {
            return new XMLHttpRequest();
        } catch (e) {
            try {
                return ActiveXObject("Msxml2.XMLHTTP");
            } catch (e) {
                try {
                    return ActiveXObject("Microsoft.XMLHTTP");
                } catch (e) {
                    alert("未知浏览器");
                    throw e;
                }
            }
        }
    }
 
    window.onload = function () {
        var provinceEle = document.getElementById("p");
        var xmlHttp = createXMLHttpRequest();
        xmlHttp.open("GET", "<c:url value='/ProvinceServlet'/>", true);
        xmlHttp.send(null);
        xmlHttp.onreadystatechange = function () {
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                var text = xmlHttp.responseText;
                var textArr = text.split(",");
                for (var i = 0; i < textArr.length; i++) {
                    var op = document.createElement("option");
                    op.value = textArr[i];
                    var textNode = document.createTextNode(textArr[i]);
                    op.appendChild(textNode);
 
                    provinceEle.appendChild(op);
                }
            }
        }
 
        provinceEle.onchange = function () {
            var xmlHttp = createXMLHttpRequest();
            xmlHttp.open("POST", "<c:url value='/CityServlet'/>", true);
            xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xmlHttp.send("province=" + provinceEle.value);
            xmlHttp.onreadystatechange = function () {
                if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                    var city = document.getElementById("c");
                    var opEleList = city.getElementsByTagName("option");
                    while (opEleList.length > 1) {
                        city.removeChild(opEleList[1]);
                    }
 
                    var doc = xmlHttp.responseXML;
                    var cityEleList = doc.getElementsByTagName("city");
                    for (var i = 0; i < cityEleList.length; i++) {
                        var cityEle = cityEleList[i];
                        var cityname;
                        if (window.addEventListener) {
                            cityname = cityEle.textContent;
                        } else {
                            cityname = cityEle.text;
                        }
                        var op = document.createElement("option");
                        op.value = cityname;
                        var textNode = document.createTextNode(cityname);
                        op.appendChild(textNode);
 
                        city.appendChild(op);
                    }
                }
            }
        }
    }
</script>
</head>
<body>
<h1>省市联动</h1><br/>
<select name="province" id="p">
    <option>===请选择省===</option>
</select>
&nbsp;
<select name="city" id="c">
    <option>===请选择市===</option>
</select>
</body>
</html>
```

ProvinceServlet.java

```java
@WebServlet(name = "ProvinceServlet", urlPatterns = {"/ProvinceServlet"})
public class ProvinceServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
        throws ServletException, IOException {
        req.setCharacterEncoding("utf-8");
        resp.setContentType("text/html;charset=utf-8");
 
        try {
            SAXReader reader = new SAXReader();
            InputStream input = this.getClass().getResourceAsStream("/china.xml");
            Document doc = reader.read(input);
 
            List<Node> arrList = doc.selectNodes("//province/@name");
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < arrList.size(); i++) {
                sb.append(arrList.get(i).getStringValue());
                if (i < arrList.size() - 1) {
                    sb.append(",");
                }
            }
            resp.getWriter().print(sb.toString());
        } catch (DocumentException e) {
            throw new RuntimeException(e);
        }
    }
}
```

CityServlet.java

```java
@WebServlet(name = "CityServlet", urlPatterns = {"/CityServlet"})
public class CityServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
        throws ServletException, IOException {
        request.setCharacterEncoding("utf-8");
        response.setContentType("text/xml;charset=utf-8");
 
        String province = request.getParameter("province");
        try {
            SAXReader reader = new SAXReader();
            InputStream input = this.getClass().getResourceAsStream("/china.xml");
            Document doc = reader.read(input);
 
            Element cities = (Element) doc.selectSingleNode("//province[@name='" + province + "']");
            String xmlStr = cities.asXML();
            response.getWriter().print(xmlStr);
        } catch (DocumentException e) {
            throw new RuntimeException(e);
        }
    }
}
```

## XStream

### 作用

把 JavaBean 转换成(序列化)成 XML。

### jar 包

- 核心 jar 包：xstream-1.4.7.jar
- 必须依赖包：xpp3_min-1.1.4c (XML Pull Parser，一款速度很快的 XML 解析器)

### 使用步骤

```java
XStream xstream = new XStream();
String xmlStr = xstream.toXML(javabeanList);
```

### 美化

- 别名：`xstream.alias("china", List.class)`
- 使用为属性：`xstream.useAttributeFor(Province.class, "name")`
- 去除 Collection 属性：`xstream.addImplicitCollection(Province.class, "cities")`
- 去除 JavaBean 中多余属性：`xstream.omitField(City.class, "description")`

**示例**

```java
public void fun5() {
    List<Province> proList = getProinvceList();
    XStream xstream = new XStream();
    /* 美化 */
    // 指定别名
    xstream.alias("china", List.class); // 给List类型指定别名为china
    xstream.alias("province", Province.class); // 给Province指定别名为province
    xstream.alias("city", City.class); // 给City类型指定别名为city
 
    // 使用为属性
    xstream.useAttributeFor(Province.class, "name"); // 把Province类型的name属性，生成<province>元素的属性
 
    // 去除Collection属性
    xstream.addImplicitCollection(Province.class, "cities"); // 去除Provice类的名为cities的List类型的属性
 
    // 去除JavaBean中多余属性
    xstream.omitField(City.class, "description"); // 让City类的，名为description属性不生成对应的xml元素
 
    String s = xstream.toXML(proList);
    System.out.println(s);       
}
```

## JSON

JSON 是 js 提供的一种数据交换格式。

### 语法

```json
{
    "null":null,
    "string":"字符串",
    "num":18,
    "array":[{...又一个json...}],
    "bool":true
}
```

### 应用

```javascript
var person = {"name":"zhangSan", "age":18, "sex":"male"};
// or
var jsonStr = "{\"name\":\"zhangSan\", \"age\":18, \"sex\":\"male\"}";
var person = eval("(" + json + ")");
```

### JSON 与 XML比较

- 可读性：XML 胜出
- 解析难度：JSON 本身就是 JS 对象(主场作战)，所以简单很多
- 流行度：XML 已经流行好多年，但在 AJAX 领域，JSON 更受欢迎

### json-lib

可以把 javabean 转换成 json 串。

### 核心类

- `JSONObject` (想象成 Map)
    - `toString()`
    - `JSONObject map = JSONObject.fromObject(person);`：把对象转换成 JSONObject 对象
- `JSONArray` (想象成 List)
    - `toString()`
    - `JSONArray jsonArray = JSONObject.fromObject(list);`：把 list 转换成 JSONArray 对象

### ajaxutils 小工具

ajaxutils.js

```javascript
/**
* 创建xmlHttp对象
* @returns {*}
*/
function createXMLHttpRequest() {
    try {
        return new XMLHttpRequest();
    } catch (e) {
        try {
            return ActiveXObject("Msxml2.XMLHTTP");
        } catch (e) {
            try {
                return ActiveXObject("Microsoft.XMLHTTP");
            } catch (e) {
                alert("未知浏览器");
                throw e;
            }
        }
    }
}
 
/**
* option里面有：
* 请求方式：method,
* 请求的url：url,
* 是否异步：asyn,
* 请求体：params,
* 回调方法：callback,
* 服务器响应数据转换成什么类型：type
*/
function ajax(option) {
    var xmlHttp = createXMLHttpRequest();
    if (option.method == undefined) {
        option.method = "GET";
    }
    if (option.asyn == undefined) {
        option.asyn = true;
    }
    xmlHttp.open(option.method, option.url, option.asyn);
    if (option.method == "POST") {
        xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    }
    xmlHttp.send(option.params);
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            var data;
            if (option.type == "xml") {
                data = xmlHttp.responseXML;
            } else if (option.type == "json") {
                var text = xmlHttp.responseText;
                data = eval("(" + text + ")");
            } else {
                data = xmlHttp.responseText;
            }
            option.callback(data);
        }
    };
}
```

ajaxutils用法：

```html
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
<title>Title</title>
<script type="text/javascript" src="<c:url value='/ajax-lib/ajaxutils.js'/>"></script>
<script type="text/javascript">
window.onload = function () {
    var btn = document.getElementById("btn");
    btn.onclick = function () {
        ajax(
            {
                url:"<c:url value="/AjaxServlet"/>",
                type:"json",
                callback:function (data) {
                    document.getElementById("h3id").innerHTML =
                    "name:" + data.name + ",age:" + data.age + ",sex:" + data.sex;
                }
            }
        );
    };
};
</script>
</head>
<body>
<h1>测试ajaxutils小工具</h1>
<button id="btn">点击这里</button>
<h3 id="h3id"></h3>
</body>
</html>
```
