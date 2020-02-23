# 第一章：Spring Framework总览 (12讲)

Java 知识点：反射、动态代理、枚举、泛型、注解、ARM、Lambda 语法。

Spring 的四个核心特性：
- IoC 容器
- Bean
- 元信息
- 基础设施

Spring 核心特性之间的联系：

Spring 可以看成一个帮我们管理 **Bean** 的框架，那么用什么管理呢？就是 **IoC 容器**。因为 Bean 是多种多样的，所以为了统一的管理这些不同种类的 Bean，我们需要给每个 Bean 装在一个统一的盒子里，这个盒子包括着一个 Bean 需要的一些 **元信息**，在配置元信息和外部化属性时，需要一些如资源管理、类型转换等工具，而提供这些工具的就是 **基础设施**。

元信息可以配置我们的 Bean，同时提供给 Bean 一些数据。

==？？？这部分关于元信息的是什么的理解需要补充，没懂==

下面就是目录，是目前的知识地图，学完一部分划掉一部分，可以清晰的知道自己的学习进度。

Spring 核心特性：
- IoC 容器（IoC Container）
- Spring 事件（Events）
- 资源管理（Resources）
- 国际化（i18n）
- 校验（Validation）
- 数据绑定（Data Binding）
- 类型装换（Type Conversion）
- Spring 表达式（Spring Express Language）
- 面向切面编程（AOP）

数据存储：

- JDBC
- 事务抽象（Transactions）
- DAO 支持（DAO Support）
- O/R映射（O/R Mapping）
- XML 编列（XML Marshalling）


Web 技术（Web）

- Web Servlet 技术栈
    - Spring MVC
    - WebSocket
- Web Reactive 技术
    - Spring WebFlux
    - WebClient
    - WebSocket


技术整合（Integration）（生态整合）

- 远程调用（Remoting）
- Java 消息服务（JMS）
- ~~Java 连接架构（JCA）~~
- Java 管理扩展（JMX）（CPU/磁盘利用率啥的）
- Java 邮件客户端（Email）（非必要）
- 本地任务（Tasks）（利用 Java 多线程，单机版，非分布式）
- 本地调度（Scheduling）（利用 Java 多线程，单机版，非分布式）
- **缓存抽象（Caching）**
- Spring 测试（Testing）


测试（Testing）

- 模拟对象（Mock Objects）
- TestContext 框架（TestContext Framework）
- Spring MVC 测试（Spring MVC Test）
- Web 测试客户端（WebTestClient）