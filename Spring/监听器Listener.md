# 监听器Listener

[TOC]

**JavaWeb 三大组件：**

- Servlet
- Listener
- Filter

三大组件的特点：除了两个感知监听器以外，都需要在 web.xml 中进行配置。

**监听器：**

- 是一个接口，内容我们自己实现
- 需要注册，比如注册在按钮上，就是监听器要监控的组件，一个事件源
- 监听器中的方法，会在相应的特殊事件发生时被调用，监听的是事件

**观察者模式：**

- 事件源
- 事件
- 监听器

## JavaWeb 中的监听器

### 事件源 (三大域)：

- **ServletContext** (服务器启动时生，关闭时死)
    - **生命周期监听：ServletContextListener**，有两个方法，一个在出生时调用，一个在死亡时调用
        - void contextInitialized(ServletContextEvent sce)：创建 Servletcontext 时
        - void contextDestroyed(ServletContextEvent sce)：销毁 Servletcontext 时
    - **属性监听：ServletContextAttributeListener**，有三个方法，分别在添加，替换，移除属性时调用
        - void attributeAdded(ServletContextAttributeEvent event)：添加属性时
        - void attributeReplaced(ServletContextAttributeEvent event)：替换属性时
        - void attributeRemoved(ServletContextAttributeEvent event)：移除属性时
- **HttpSession** (有客户端访问时生)
    - **生命周期监听：HttpSessionListener**，有两个方法，一个在出生时调用，一个在死亡时调用
        - void sessionCreated(HttpSessionEvent se)：创建 session 时
        - void sessionDestroyed(HttpSessionEvent se)：销毁 session 时
    - **属性监听：HttpSessionAttributeListener**，有三个方法，分别在添加，替换，移除属性时调用
        - void attributeAdded(HttpSessionBindingEvent event)：添加属性时
        - void attributeReplaced(HttpSessionBindingEvent event)：替换属性时
        - void attributeRemoved(HttpSessionBindingEvent event)：移除属性时
- **ServletRequest** (有请求就生)
    - **生命周期监听：ServletRequestListener**，有两个方法，一个在出生时调用，一个在死亡时调用
        - void requestInitialized(ServletRequestEvent sre)：创建 request 时
        - void requestDestroyed(ServletRequestEvent sre)：销毁 request 时
    - **属性监听：ServletRequestAttributeListener**，有三个方法，分别在添加，替换，移除属性时调用
        - void attributeAdded(ServletRequestAttributeEvent srae)：添加属性时
        - void attributeReplaced(ServletRequestAttributeEvent srae)：替换属性时
        - void attributeRemoved(ServletRequestAttributeEvent srae)：移除属性时

### JavaWeb 中编写监听器

- 写一个监听器类 (实现某个监听器接口)

    ```java
    public class Alistener implements ServletContextListener {
        @Override
        public void contextInitialized(ServletContextEvent servletContextEvent) {
            // 可以在这个监听器存放一些在tomcat启动时就要完成的代码
            System.out.println("I'm coming...");
        }
 
        @Override
        public void contextDestroyed(ServletContextEvent servletContextEvent) {
            System.out.println("I'm leaving...");
        }
    }
    ```

- 注册，在 web.xml 中配置来完成注册

    ```xml
    <listener>
        <listener-class>priv.bean.web.listener.AListener</listener-class>
    </listener>
    ```

### 事件对象

- **Event：**
    - **ServlerContextEvent**：ServletContext getServletContext()
    - **HttpSessionEvent**：HttpSession getSession()
    - **ServletRequest**：
      - ServletContext getServletContext()
      - ServletRequest getServletRequest()
- **AttributeEvent：**
    - **ServletContextAttributeEvent**：
        - ServletContext getServletContext()
        - String getName()：获取属性名
        - Object getValue()：获取属性值

### 感知监听器 HttpSessionBindingListener

- HttpSessionBindingListener 是和 session 相关的
- 感知监听器是用来添加到 JavaBean 上的，而不是三大域上的
- 不需要在 web.xml 中注册
- 接口 (不常用，用了就绑死了，以后离不开了)
    - HttpSessionBindingListener：添加到 JavaBean 上，JavaBean 就知道自己是否添加到 session 中了，这样 JavaBean 就知道自己是否被添加到 session 中了。
        - void valueBound(HttpSessionBindingEvent event)：session 添加了我
        - void valueUnbound(HttpSessionBindingEvent event)：session 移除了我

### 钝化活化监听器 HttpSessionActivationListener

- HttpSessionActivationListener 是和 session 相关的

- HttpSessionActivationListener 是用来添加到 JavaBean 上的，对于实现了这个接口的 JavaBean，当它被添加到 session 域中并较长时间没有被访问到时，为了节约内存，它会随着 session 一起被序列化到硬盘上，因此实现了这个接口的 JavaBean 需要具有能被序列化的能力，也就是说**这个 JavaBean 应该实现了Serializable 接口**。

- 不需要在 web.xml 中注册，但要在 context.xml 中进行如下配置，其中 maxIdleSwap="1" 的单位是分钟

    ```xml
    <Context>
        <Manager className="org.apache.catalina.session.PersistentManager" maxIdleSwap="1">
            <Store className="org.apache.catalina.session.FileStore" directory="mysession"/>
        </Manager>
    </Context>
    ```

- 接口中的方法：

    ```java
    public void sessionWillPassivate(HttpSessionEvent evt) {
        System.out.println("session被钝化了！");
    }
 
    public void sessionDidActivate(HttpSessionEvent evt) {
        System.out.println("session已经活化");
    }
    ```