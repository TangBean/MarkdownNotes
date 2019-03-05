# Servlet

[TOC]

## Servlet 概述

Servlet 是 Java 的三大组件之一，是动态资源，作用是**处理请求**，服务器会把接收到的请求交给Servlet来处理。

Servlet 需要完成：

- 接收请求数据
- 处理请求
- 完成响应

Servlet由我们自己编写，实现`javax.servlet.Servlet`接口。

**特性：**

- **单例**的典型应用，一个类只有一个对象，当然可能存在多个Servlet类
- **线程不安全**，所以效率高

## 实现 Servlet 的方式

实现Servlet由三种方式：

- 实现`javax.servlet.Servlet`接口
- 继承`javax.servlet.GenericServlet`抽象类
- 继承`javax.servlet.http.HttpServlet`类（以后比较常用的，就好比我们要用List的时候一般都直接用ArrayList一样）

## Servlet 接口

一共有5个方法：

```java
public interface Servlet {
    public void init(ServletConfig config) throws ServletException;
    *** public ServletConfig getServletConfig();  // 获取配置
    *** public void service(ServletRequest req, ServletResponse res)
                throws ServletException, IOException;
    public String getServletInfo();  // 一个对该Servlet类的描述，没啥用
    *** public void destroy();
}
```

其中有3个是生命周期方法：

- `void init(ServletConfig config)`：在Servlet创建后执行一次
- `void service(ServletRequest req, ServletResponse res)`：每次处理请求都会被调用
- `void destroy()`：在Servlet被销毁前执行，用来说遗言的，一般在关闭Tomcat时Servlet被销毁

## web.xml 配置方法

![web.xml配置方法](http://ox7712i91.bkt.clouddn.com/web.xml%E9%85%8D%E7%BD%AE%E6%96%B9%E6%B3%95.png)

**原理：**反射，一个模仿Tomcat运行Servlet的程序：ReflectDemo.java，ClassDemo.java (见附件)

## ServletConfig 接口

一个ServletConfig对象对应一段web.xml中的`<servlet> ... </servlet>`配置信息。

![ServletConfig是什么](http://ox7712i91.bkt.clouddn.com/ServletConfig%E6%98%AF%E4%BB%80%E4%B9%88.png)

**API**

- `String getServletName()`：获取`<servlet-name>`中内容
- `ServletContext getServletContext()`：获取Servlet上下文
- `String getInitParameter(String name)`：通过xml标签的名称获取`<init-param>`标签中指定的初始化内容
- `Enumeration getInitParameterNames()`：获取所有初始化参数，就是当前配置文件中所有`<init-param>`标签中的内容


## GenericServlet

由`javax.servlet.Servlet`接口可以看出，如果每一次要创建一个Servlet都要把里面的5个方法都实现一遍是十分麻烦的，所以除了通过实现Servlet接口创建Servlet，我们还可以通过继承GenericServlet抽象类的方法来创建Servlet，使用这种方法我们可以只重写我们需要的类，而不用把我们不需要的类也重写一遍。

除此之外，GenericServlet还提供了许多其他的方法，比如`getInitParameter(java.lang.String name)` ，`getInitParameterNames()`，`getServletName()`，`getServletContext()`等一系列获取当前Servlet配置信息的方法。

GenericServlet之所以能实现这些方法是因为：它由一个private的成员变量`ServletConfig config`，它在实现Servlet接口的`void init(ServletConfig config)`方法时，做的第一件事是`this.config = config`，所以之后只要通过获取当前Servlet类中的config成员变量就可以获取到Servlet的各种配置信息了。

但是，这样做有一个问题是，当我们通过继承GenericServlet来实现我们自己的Servlet时，我们有的时候是需要重写`void init(ServletConfig config)`方法的，如果我们没有写`this.config = config`，那么那些关于config的方法就无法执行了，这是什么不安全的，所以GenericServlet又写了一个没有传入参数的`void init()`方法，然后在`void init(ServletConfig config)`中调用它。我们在重写init方法时重写的是没有参数列表的`void init()`方法，这样就不会影响config的初始化操作了。

`void init(ServletConfig config)`方法和`void init(ServletConfig config)`方法的实现如下：

```java
private transient ServletConfig config;
 
public void init(ServletConfig config) throws ServletException {
    this.config = config;
    this.init();
}
 
public void init() throws ServletException {
    // NOOP by default
}
```

## HttpServlet

是一个继承`GenericServlet`的抽象类，虽然是一个抽象类，但是没有一个抽象方法，看名字就知道这个类是专门为HTTP协议准备的。

它的原理如下：

```java
public abstract class HttpServlet extends GenericServlet {
    protected void service(HttpServletRequest req, HttpServletResponse resp)
        throws ServletException, IOException {
        /*
        在这里参数已经是Http相关的了，它会通过request得到当前的请求方式，在根据请求方式判断是调用
        doGet还是doPost，还是什么其他的
        */
        String method = req.getMethod();
        if (method.equals(METHOD_GET)) {
            /* 省略 balabala... */
            doGet(req, resp);
        } else if (method.equals(METHOD_POST)) {
            doPost(req, resp);
        }
    }
 
    public void service(ServletRequest req, ServletResponse res)
        throws ServletException, IOException {
 
        HttpServletRequest  request;
        HttpServletResponse response;
        // 在这里强转成Http相关，然后调用 void service(HttpServletRequest req, HttpServletResponse resp)
        try {
            request = (HttpServletRequest) req;
            response = (HttpServletResponse) res;
        } catch (ClassCastException e) {
            throw new ServletException("non-HTTP request or response");
        }
        service(request, response);
    }
}
```

**注意：**doGet和doPost由我们自己来覆盖！如果我们没有覆盖doGet或doPost，并且它们还被调用了，会出现405，说明该Servlet不支持该请求方式。

## Servlet 的一些其他问题

### Servlet 的线程安全问题

Servlet 只有一个实例对象，所以可能会出现一个 Servlet 同时处理多个请求，但 Servlet 是线程不安全的 (所以它工作效率高)，因此我们尽可能不要在 Servlet 中创建成员变量，或者只创建只读 (只能 get 不能 set) 的成员变量来保证线程线程安全。

### 在服务器启动时创建 Servlet

默认情况下，服务器会在某个Servlet第一次收到请求时创建它。也可以在web.xml中对Servlet进行配置，使服务器启动时就创建Servlet。配置方法如下：在`<load-on-startup>0</load-on-startup>`中填入一个非负整数，这个数越小越先被启动。

```xml
<servlet>
    <servlet-name>hello1</servlet-name>
    <servlet-class>cn.itcast.servlet.Hello1Servlet</servlet-class>
    <load-on-startup>0</load-on-startup>  <!-- 第一个被启动 -->
</servlet>
<servlet-mapping>
    <servlet-name>hello1</servlet-name>
    <url-pattern>/hello1</url-pattern>
</servlet-mapping>
 
<servlet>
    <servlet-name>hello2</servlet-name>
    <servlet-class>cn.itcast.servlet.Hello2Servlet</servlet-class>
    <load-on-startup>1</load-on-startup>  <!-- 第二个被启动 -->
</servlet>
<servlet-mapping>
    <servlet-name>hello2</servlet-name>
    <url-pattern>/hello2</url-pattern>
</servlet-mapping>
 
<servlet>
    <servlet-name>hello3</servlet-name>
    <servlet-class>cn.itcast.servlet.Hello3Servlet</servlet-class>
    <load-on-startup>2</load-on-startup>  <!-- 第三个被启动 -->
</servlet>
<servlet-mapping>
    <servlet-name>hello3</servlet-name>
    <url-pattern>/hello3</url-pattern>
</servlet-mapping>
```

### 多个 `url-pattern`

`<url-pattern>`是`<servlet-mapping>`的子元素，用来指定Servlet的访问路径，即URL。它必须是以`/`开头的。

可以在一个`<servlet-mapping>`中给出多个`<url-pattern>`，例如

```xml
<servlet-mapping>
    <servlet-name>AServlet</servlet-name>
    <url-pattern>/AServlet</url-pattern>
    <url-pattern>/BServlet</url-pattern>
</servlet-mapping>
```

说明一个Servlet绑定了两个URL，无论访问`/AServlet`还是`/BServlet`，访问的都是`AServlet`。

除此之外，还可以在`<url-pattern>`中使用通配符`*`：

- `<url-pattern>/servlet/*</url-pattern>`：路径匹配
- `<url-pattern>*.do</url-pattern>`：扩展名匹配
- `<url-pattern>/*</url-pattern>`：匹配所有URL

**注意：**

- 通配符要么为前缀，要么为后缀，不能出现在URL中间位置，也不能只有通配符。例如：`/*.do`就是错误的，因为星号出现在URL的中间位置上了。`*.*`也是不对的，因为一个URL中最多只能出现一个通配符。
- 如果出现URL符合多个匹配模式的情况，URL会去匹配最具体的那个，也就是能匹配的模式最少的那个。

## ServletContext

### ServletContext 概述

- 一个项目只有一个ServletContext对象，服务器会为每一个应用创建一个ServletContext对象，也就是说，一个项目中的Servlet可以通过这个ServletContext对象进行通信，交换数据
- 天地同寿，ServletContext对象在服务器启动时创建，在服务器关闭时销毁

### 获取 ServletContext 对象

有好多个接口或者类的`getServletContext()`方法都能获取ServletContext对象：

- `ServletConfig#getServletContext()`
- `GenericServlet#getServletContext()`
- `HttpSession#getServletContext()`
- `ServletContextEvent#getServletContext()`

### 域对象的功能

- 域对象就是用来在多个Servlet中传递数据，因此它一定有存数据和取数据这两个功能
- 域对象内部其实有一个Map，用来存储键值对

**JavaWeb 四大域对象**

- `PageContext`
- `ServletRequest`
- `HttpSession`
- `ServletContext`

**ServletContext 对象操作数据的方法：**

- `void setAttribute(String name, Object value)`：存储一个键值对
- `Object getAttribute(String name)`：根据key获取ServletContext中存储的值
- `void removeAttribute(String name)`：根据key删除ServletContext中的数据
- `Enumeration getAttributeNames()`：获取ServletContext中存储的所有键值对的keys的集合

### 获取应用的初始化参数

- Servlet也可以获取初始化参数，但它是局部的参数；也就是说，一个Servlet只能获取自己的初始化参数，不能获取别人的，即初始化参数只为一个Servlet准备。
- 可以配置公共的初始化参数，为所有Servlet而用。这需要使用ServletContext才能使用。

**公共初始化参数配置方法：**在根标签的`<context-param></context-param>`标签下

```xml
<web-app>
    ...
    <context-param>
        <param-name>paramName1</param-name>
        <param-value>paramValue1</param-value>     
    </context-param>
    <context-param>
        <param-name>paramName2</param-name>
        <param-value>paramValue2</param-value>     
    </context-param>
</web-app>
```

**公共初始化参数的获取方法：**

```java
ServletContext context = this.getServletContext();
String value1 = context.getInitParameter("paramName1");
String value2 = context.getInitParameter("paramName2");
System.out.println(value1 + ", " + value2);
 
Enumeration names = context.getInitParameterNames();
while(names.hasMoreElements()) {
    System.out.println(names.nextElement());
}
```

### 获取资源

#### 获取真实路径

```java
String realPath = servletContext.getRealPath(“/a.txt”);  // 得到的是一个带盘符的绝对路径
```

#### 获取资源流

```java
InputStream in = servletContext.getResourceAsStream(“/a.txt”);
```

#### 获取指定目录下的所有资源路径

```java
Set set = context.getResourcePaths("/WEB-INF");  // 返回的是一个Set
```

## BaseServlet

### 概述

- 目的是实现可以在一个 Servlet 中有多个请求处理方法
- 客户端发送请求时，需要给出一个参数，用来说明要调用的方法
- 请求处理方法的签名必须与 Servlet 的 service 方法相同，即返回值和参数，以及声明的异常都相同
- 方法的调用通过反射来实现
- 过程中会抛出3个异常
    - 请求没有给出 method 参数
    - 调用的方法不存在
    - 调用的方法运行过程中出现异常

### 代码

BaseServlet 是一个继承自 HttpServlet 的抽象类，以后我们要写 Servlet 的时候就直接继承 BaseServlet 就可以了。

```java
public abstract class BaseServlet extends HttpServlet {
    @Override
    protected void service(HttpServletRequest req, HttpServletResponse resp)
        throws ServletException, IOException {
        String methodName = req.getParameter("method");
 
         // 第一个异常
        if (methodName == null) {
            throw new RuntimeException("没有传入方法名");
        }
 
        // 第二个异常
        Class clazz = this.getClass();
        Method method = null;
        try {
            method = clazz.getMethod(methodName, HttpServletRequest.class, HttpServletResponse.class);
        } catch (NoSuchMethodException e) {
            throw new RuntimeException("方法" + methodName + "不存在");
        }
 
        // 第三个异常
        try {
            String result = (String) method.invoke(this, req, resp);
            if (result == null || result.trim().length() == 0) {
                return;
            }
            if (result.contains(":")) {
                int index = result.indexOf(":");
                String s = result.substring(0, index);
                String path = result.substring(index + 1);
                if (s.equalsIgnoreCase("f")) {
                    req.getRequestDispatcher(path).forward(req, resp);
                } else if (s.equalsIgnoreCase("d")) {
                    resp.sendRedirect(req.getContextPath() + path);
                } else {
                    throw new RuntimeException("指定操作" + s + "不存在");
                }
            } else {
                req.getRequestDispatcher(result).forward(req, resp);
            }
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
```

BaseServlet 的用法：

```java
public class AServlet extends BaseServlet {
    public String fun1(HttpServletRequest req, HttpServletResponse resp) {
        System.out.println("fun1()...");
        return "f:/index.jsp";
    }
 
    public String fun2(HttpServletRequest req, HttpServletResponse resp) {
        System.out.println("fun2()...");
        return "d:/index.jsp";
    }
 
    public String fun3(HttpServletRequest req, HttpServletResponse resp) {
        System.out.println("fun3()...");
        return "/index.jsp";
    }
}
```

## 补充：获取类路径下的资源

类路径对一个JavaWeb项目而言，就是`/WEB-INF/classes`和`/WEB-INF/lib/每个jar包`，可以通过**Class类**或者**ClassLoader类**获取。

### Class 类获取

```java
InputStream in = this.getClass().getResourceAsStream("/xxx.txt");
System.out.println(IOUtils.toString(in));
```

**注意：**

- 路径以`/`开头，指相对于classes的路径
- 路径不以`/`开头，指相对于当前class文件所在的路径

### ClassLoader 类获取

```java
InputStream in = this.getClass().getClassLoader().getResourceAsStream("xxx.txt");
System.out.println(IOUtils.toString(in));
```

- 指相对于classes的路径