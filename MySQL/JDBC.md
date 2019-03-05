# JDBC

[TOC]

## Java连接数据库

**步骤：**

- 导包：`mysql-connector-java-5.1.13-bin.jar`
- 加载驱动类 (注册驱动)
- 给出 url，username，password
- 通过 DriverManager 获取 Connection 对象

**四大配置参数：**

| 参数名称        | 参数值                                |
| --------------- | ------------------------------------- |
| driverClassName | `"com.mysql.jdbc.Driver"`             |
| url             | `"jdbc:mysql://localhost:3306/mydb1"` |
| username        | `"root"`                              |
| password        | `"123"`                               |

**两个抛出的异常：**

- `ClassNotFoundException`：driverClassName 有问题
- `SQLException`：url，username，password 有问题，或者数据库根本没开

**代码示例：**

```java
Class.forName("com.mysql.jdbc.Driver");
Connection con = DriverManager.getConnection("jdbc:mysql://localhost:3306/mydb1", "root", "123");
```

## JDBC原理

Java 连接到数据库的两条语句看似关系不大是因为：

```java
// Class.forName("com.mysql.jdbc.Driver");
// 上面的这句等同于：
com.mysql.jdbc.Driver driver = new com.mysql.jdbc.Driver();
DriverManager.registerDriver(driver);
 
Connection con = DriverManager.getConnection("jdbc:mysql://localhost:3306/mydb1", "root", "123");
```

`Class.forName("com.mysql.jdbc.Driver");`的原理是：所有的 java.sql.Driver 实现类，都提供了static 块，块内的代码就是把自己注册到 DriverManager 中。也就是说在 com.mysql.jdbc.Driver 的实现中有一个静态代码块写着：

```java
com.mysql.jdbc.Driver driver = new com.mysql.jdbc.Driver();
DriverManager.registerDriver(driver);
```

然后 Class.forName() 在加载类的时候会执行这个静态代码块，就把自己注册到了 DriverManager 中。

不过在 jdbc4.0 之后就不用再写加载驱动这句了，因为 jdbc4.0 之后，每个驱动 jar 包中，在 META-INF/services 目录下提供了一个名为 java.sql.Driver 的文件，这个文件中写着 java.sql.Driver 接口的实现类名称，如：com.mysql.jdbc.Driver。

不过为了通用性最好还是把加载驱动这句写上。

## JDBC的增删改查

JDBC 的增删改查的本质是通过数据库自己的语法实现的，我们只需要把相应的数据库语句发送给我们连接上的数据库即可。

### 要用到的三个主要对象

对于通过 Java 对数据库进行操作，我们主要需要以下三个对象，这三个对象用完是要关的，如果不关会耗费系统资源：

- 连接对象：Connection

    ```java
    Connection con = DriverManager.getConnection(url, username, password);
    ```

- 语句发送器对象：Statement，主要用来向数据库发送 SQL 语句，通过它可以实现数据库的 DML 和 DDL 了

    ```java
    Statement stmt = con.createStatement();
    String sql = ...;
    int r = stmt.executeUpdate(sql);  // 执行这条SQL语句，会返回一个int，表示改变的列数
    ```

- 查询结果对象：ResultSet，存着查到的表的信息

    ```java
    ResultSet rs = stmt.executeQuery("select * from emp");
    ```

    - 解析方法：![ResultSet结构](http://ox7712i91.bkt.clouddn.com/ResultSet%E7%BB%93%E6%9E%84.jpg)

- 关闭资源：要倒着关

    ```java
    rs.close();
    stmt.close();
    con.close();
    ```

### 示例

**增删改示例：**

```java
public void fun1() throws ClassNotFoundException, SQLException {
    // 准备4大参数
    String driverClassName = "com.mysql.jdbc.Driver";
    String url = "jdbc:mysql://localhost:3306/mydb3";
    String username = "root";
    String password = "123";
 
    // 得到连接对象：Connection
    Class.forName(driverClassName);
    Connection con = DriverManager.getConnection(url, username, password);
 
    // 得到Statement对象
    Statement stmt = con.createStatement();
 
    // 增
    String sqlIn = "INSERT INTO stu VALUES('ITCAST_0003', 'wangWu', 88, 'male')";
    int rIn = stmt.executeUpdate(sqlIn);
 
    // 改
    String sqlCh = "UPDATE stu SET name='zhaoLiu', age=22, " +
        "gender='female' WHERE number='ITCAST_0003'";
    int rCh = stmt.executeUpdate(sqlCh);
 
    // 删
    String sqlDe = "DELETE FROM stu";
    int rDe = stmt.executeUpdate(sqlDe);
}
```

**查示例：**

```java
public void fun2() throws ClassNotFoundException, SQLException {
    String driverClassName = "com.mysql.jdbc.Driver";
    String url = "jdbc:mysql://localhost:3306/exam";
    String username = "root";
    String password = "123";
 
    Class.forName(driverClassName);
    Connection con = DriverManager.getConnection(url, username, password);
 
    Statement stmt = con.createStatement();
 
    // 得到查询结果对象
    ResultSet rs = stmt.executeQuery("select * from emp");
 
    // 解析ResultSet
    while (rs.next()) {
        int empno = rs.getInt(1);  // 通过列编号来获取该列的值
        String ename = rs.getString("ename");  // 通过列名称来获取该列的值
        double sal = rs.getDouble("sal");
        System.out.println(empno +  ", " + ename + ", " + sal);
    }
 
    // 关资源
    rs.close();
    stmt.close();
    con.close();  //这个东东，必须要关，一个不定时炸弹！
}
```

## JDBC代码规范化

我们要保证 Connection，Statement，ResultSet 这几个资源肯定关了，所以要把它们放到 finally 块里去。规范写法如下：

```java
public void fun3() throws Exception {
    Connection con = null;
    Statement stmt = null;
    ResultSet rs = null;
    try {
        String driverClassName = "com.mysql.jdbc.Driver";
        String url = "jdbc:mysql://localhost:3306/exam";
        String username = "root";
        String password = "123";
 
        Class.forName(driverClassName);
        con = DriverManager.getConnection(url, username, password);//实例化
 
        stmt = con.createStatement();
        String sql = "select * from emp";
        rs = stmt.executeQuery(sql);
        // 注意：getString()和getObject()是通用的！
        while (rs.next()) {
            System.out.println(rs.getObject(1) + ", "
                    + rs.getString("ename") + ", " + rs.getDouble("sal"));
        }
    } catch (Exception e) {
        throw new RuntimeException(e);
    } finally {
        // 关闭，要先判断是不是空的，不是空的才能关
        if (rs != null) rs.close();
        if (stmt != null) stmt.close();
        if (con != null) con.close();
    }
}
```

## JDBC对象介绍

**JDBC的常用类(接口)：**

- DriverManager
- Connection
- Statement
- ResultSet

### DriverManager

主要用它的 getConnection() 方法获取 Connection 类：

```java
Class.forName("com.mysql.jdbc.Driver");  // 可能抛出ClassNotFoundException
String url = "jdbc:mysql://localhost:3306/mydb1";
String username = "root";
String password = "123";
Connection con = DriverManager.getConnection(url, username, password);  // 可能抛出SQLException
```

对于 DriverManager.registerDriver() 了解即可，不太会用到，不过要明白不同数据库的驱动的注册机制。

### Connection

最主要的用途就是获取 Statement 对象，有两种获取方法：

```java
Statement stmt = con.createStatement();
Statement stmt = con.createStatement(int resultSetType, int resultSetConcurrency);
```

- 第一个方法比较常用，能获取到一个能查询**不滚动，不敏感，不更新**的结果集的 Statement
- 第二个方法可以根据需要传入不同的参数，以获得带有不同属性的结果集：
    - 第一个参数：resultSetType
        - `ResultSet.TYPE_FORWARD_ONLY`：不滚动结果集
        - `ResultSet.TYPE_SCROLL_INSENSITIVE`：滚动结果集，结果集数据不会再跟随数据库而变化
        - `ResultSet.TYPE_SCROLL_SENSITIVE`：滚动结果集，结果集数据会再跟随数据库而变化(一般数据库不实现)
    - 第二个参数：resultSetConcurrency
        - `ResultSet.CONCUR_READ_ONLY`：结果集的更新不会反向影响数据库
        - `ResultSet.CONCUR_UPDATABLE`：结果集的更新可以反向影响数据库(基本没数据库实现呀)

滚动结果集和不滚动结果集的区别在 ResultSet 小节中说明。

### Statement

最重要的两个方法：

```java
// 执行insert，update，delete语句，返回SQL语句影响数据库的行数:
int lines = stmt.executeUpdate(String sql);
// 执行query语句，返回ResultSet结果集
ResultSet rs = stmt.executeQuery(String sql);
```

其实 Statement 类还有一个 boolean execute() 方法，这个方法可以执行所有 SQL 语句，不分类型，不过它只返回该 SQL 语句执行完之后是否有结果集

- 对于更新语句，还需要调用 int getUpdateCount() 方法获取语句所影响的行数
- 对于查询语句，还需要调用 ResultSet getResultSet() 方法获取 select 语句的查询结果

所以，boolean execute() 方法很鸡肋，基本不用。

### ResultSet

ResultSet 表示结果集，是一个二维表格，其内部维护一个行光标，ResultSet 提供了一系列方法来移动行光标，这些方法根据结果集是滚动的还是不滚动的分为如下两种：

**不滚动和滚动都可以执行的方法：**

- 移动光标的方法

  ```java
  boolean next()  // 把光标向下挪一行
  // 虚拟位置
  void beforeFirst()  // 把光标放到第一行的前面(光标的默认位置)
  void afterLast()  // 把光标放到最后一行的后面
  // 真实位置
  boolean first()  // 把光标放到第一行的位置上，返回值表示调控光标是否成功
  boolean last()  // 把光标放到最后一行的位置上
  ```

- 判断光标位置的方法

    ```java
    boolean isBeforeFirst()  // 当前光标位置是否在第一行前面
    boolean isAfterLast()  // 当前光标位置是否在最后一行的后面
    boolean isFirst()  // 当前光标位置是否在第一行上
    boolean isLast()  // 当前光标位置是否在最后一行上
    int getRow()  // 返回当前光标所有行
    ```

- 获取列数据，ResultSet 可以通过列的引索(注意：列引索从 1 开始，而不是从 0 开始，和 Matlab 一样哈)，或者通过列名称来获取行光标所在的行的列数据

    ```java
    String getString(int columnIndex / String columnName)
    int getInt(int columnIndex / String columnName)
    double getDouble(int columnIndex / String columnName)
    boolean getBoolean(int columnIndex / String columnName)
    Object getObject(int columnIndex / String columnName)
    ```


**只有滚动的结果集才可以执行的方法：**

- 随意移动光标，只有滚动的结果集才能这么干，不滚动的结果集就像象棋中的"卒"，只能向前走，不能往回走

    ```java
    boolean previous()  // 把光标向上挪一行
    boolean relative(int row)  // 相对位移，当row为正数时，表示向下移动row行，为负数时表示向上移动row行
    boolean absolute(int row)  // 绝对位移，把光标移动到指定的行上
    ```

### PreparedStatement

PreparedStatement 是 Statement 接口的子接口，叫预编译声明。

**PreparedStatement的用处：**

- 防 SQL 攻击
- 提高代码可读性，可维护性
- 提高效率

在以后开发中，都要选择使用 PreparedStatement 而不是 Statement。

#### PreparedStatement打开方式

默认 mysql 是关闭预处理的，要通过给 url 加参数的方式打开：`jdbc:mysql://localhost:3306/exam?useServerPrepStmts=true&cachePrepStmts=true`。

#### PreparedStatement用法

- 给出 SQL 模板，SQL 模板就是有 "?" 的 SQL 语句，"?" 代表参数
- 调用 Connection 的 preparedStatement(String sql) 方法，得到 PreparedStatement 对象
- 调用 PreparedStatement 的 setXXX() 系列方法为问号设置值，例如第一个参数就是：pstmt.setXXX(1, xxx)
- 调用 executeUpdate() 或 executeQuery() 方法，因为已经把要执行的 SQL 语句传进去了，所以不用传入参数

**示例：**

```java
public void fun1() throws ClassNotFoundException, SQLException {
    Class.forName("com.mysql.jdbc.Driver");
    String url = "jdbc:mysql://localhost:3306/exam";
    String username = "root";
    String password = "123";
    Connection con = DriverManager.getConnection(url, username, password);
 
    // 给出SQL模板
    String sql = "SELECT * FROM stu WHERE sname=? AND sid=?";
    // 得到PreparedStatement对象
    PreparedStatement pstmt = con.prepareStatement(sql);
    // 调用PreparedStatement的setXXX()系列方法为问号设置值
    pstmt.setString(1, "王永");
    pstmt.setInt(2, 1);
    // 执行SQL语句
    ResultSet rs = pstmt.executeQuery();
 
    System.out.println(rs.next());
    rs.close();
    pstmt.close();
    con.close();
}
```

#### PreparedStatement的原理

**服务器的工作原理：**

- 校验 SQL 语法是否正确
- 编译这个 SQL 语句：得到一个和函数相似的东西，就等值执行的时候把参数往里面一传
- 执行：调用编译时得到的函数

**PreparedStatement的工作原理：**

- 每个 pstmt 都与一个 SQL 模板绑定，pstmt 先把模板传给数据库，数据库先对模板进行校验，并进行编译
- 执行编译时得到的函数

**PreparedStatement效率高的原因：**

在第二次执行时，不需要再次校验语法以及编译，直接传入参数执行，所以效率高。

#### 预处理防SQL攻击原理

```java
/**
* 我们传入如下参数：
* sname = "hello' OR 'a'='a";
* psword = "hello' OR 'a'='a";
* 函数运行后，会输出true
*/
public void funSQLAttack(String sname, String psword) throws ClassNotFoundException, SQLException {
    Class.forName("com.mysql.jdbc.Driver");
    String url = "jdbc:mysql://localhost:3306/exam";
    String username = "root";
    String password = "123";
    Connection con = DriverManager.getConnection(url, username, password);
    Statement stmt = con.createStatement();
    String sql = "SELECT * FROM stu WHERE sname='" + sname + "' AND province='" + psword + "'";
    System.out.println(sql);
    ResultSet rs = stmt.executeQuery(sql);
    System.out.println(rs.next());
    rs.close();
    stmt.close();
    con.close();
}
```

我们通过在用户名和密码中添加字符`'`，提前结束了字符串，并在它后面加上了永远为 true 的判断，这样即使不知道正确的用户名和密码也能通过测试，这就是 SQL 攻击。

**防止 SQL 攻击的方法：**

- 过滤用户输入的数据中是否包含非法字符，有`'`就不通过
- 分步交验，先使用用户名来查询用户，如果查找到了，再比较密码
- 使用 PreparedStatement

## JDBCUtils工具类

连接数据库的四大参数是：驱动类，url，用户名，密码，这些都是固定的，我们可以通过修改这些参数来选择连接不同的数据库，为了之后可以十分方便的连接各种数据库，我们可以把数据库的连接封装成工具类。

```java
public class JDBCUtils {
    private static final String dbconfig = "dbconfig.properties";
    private static Properties properties = new Properties();
 
    static {
        try {
            InputStream in = JDBCUtils.class.getClassLoader().getResourceAsStream(dbconfig);
            properties.load(in);
            Class.forName(properties.getProperty("driverClassName"));
        } catch (IOException e) {
            throw new RuntimeException(e);
        } catch (ClassNotFoundException e) {
            throw new RuntimeException(e);
        }
    }
 
    public static Connection getConnection() {
        try {
            return DriverManager.getConnection(properties.getProperty("url"),
                    properties.getProperty("username"), properties.getProperty("password"));
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }
}
/**
dbconfig.properties配置文件：
driverClassName=com.mysql.jdbc.Driver
url=jdbc:mysql://localhost:3306/exam?useServerPrepStmts=true&cachePrepStmts=true
username=root
password=123
*/
```

**为什么要加载类驱动的部分放到静态代码块中？**

因为我们可能需要多次调用 getConnection() 方法，而加载类驱动部分的代码只需要执行一次，因此把它放在 getConnection() 方法会导致效率降低，而 getConnection() 方法又是一个静态方法，不创建对象直接通过类名也可以调用，因此也不能把加载类驱动部分的代码放在构造函数中。**因此我们需要一种能对类进行初始化的方法，静态代码块是最好的选择，静态代码块是给类初始化的，随着类的加载而执行，只执行一次，并优先于主函数。**(P.S. 构造代码块，相比静态代码块就是没有 static 关键字，是给对象初始化的)

## DAO模式

DAO (Data Access Object)，就是写一个类，把访问数据库的代码封装起来，不过我们访问的数据库可能是不确定的，如果在代码里面写好了依赖于某个数据库的实现类，那么如果以后要换数据库会很不方便，因此我们应该写一个 Dao 接口，需要操作 Domain 的 DaoImpl 类都应当实现这个 Dao 接口，然后我们通过修改配置文件选择不同的 DaoImpl 实现类，我们不在代码中通过 new 来得到这个 DaoImpl 类的对象，而是创建一个 DaoFactory 类，这个 DaoFactory 类通过反射的方法从配置文件中读取到我们要的类的类名，通过 Class.forname() 将其加载进来，然后通过 newInstance() 方法来得到 DaoImpl 类的方法。

也就是说，我们要进行如下步骤：

- 提供一个用来操作 Domain 的 DAO 接口
- 提供一个该 DAO 接口的实现类
- 写一个该接口的 DAO 工厂类，Service 通过工厂类来获取 DAO 实现，该工厂类可以通过配置文件选择产生不同的 DAO 接口实现类

**示例：**

UserDao.java

```java
public interface UserDao {
    public void add(User user);
    public User findUserByUsername(String username);
}
```

UserDaoMysqlImpl.java

```java
public class UserDaoMysqlImpl implements UserDao {
    @Override
    public void add(User user) {
        Connection con = null;
        PreparedStatement pstmt = null;
        try {
            con = JDBCUtils.getConnection();
            String addSql = "insert into `user` (username, password) value(?, ?)";
            pstmt = con.prepareStatement(addSql);
            pstmt.setString(1, user.getUsername());
            pstmt.setString(2, user.getPassword());
            pstmt.executeUpdate();
        } catch (SQLException e) {
            throw new RuntimeException(e);
        } finally {
            try {
                if (pstmt != null) {
                    pstmt.close();
                }
                if (con != null) {
                    con.close();
                }
            } catch (SQLException e) {
                throw new RuntimeException(e);
            }
        }
    }
 
    @Override
    public User findUserByUsername(String username) {
        Connection con = null;
        PreparedStatement pstmt = null;
        ResultSet res = null;
        User user = null;
        try {
            con = JDBCUtils.getConnection();
            System.out.println(con == null);
            String queryByNameSql = "select * from `user` where username=?";
            pstmt = con.prepareStatement(queryByNameSql);
            pstmt.setString(1, username);
            res = pstmt.executeQuery();
            if (res.next()) {
                user = new User();
                user.setUsername(res.getString("username"));
                user.setPassword(res.getString("password"));
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        } finally {
            try {
                if (res != null) {
                    res.close();
                }
                if (pstmt != null) {
                    pstmt.close();
                }
                if (con != null) {
                    con.close();
                }
            } catch (SQLException e) {
                throw new RuntimeException(e);
            }
        }
        return user;
    }
}
```

UserDaoFactory.java

```java
/**
* dao.properties文件中这么配置：
* cn.bean.user.dao.UserDao=cn.bean.user.dao.UserDaoMysqlImpl
*/
public class UserDaoFactory {
    private static UserDao userDao;
 
    static {
        try {
            InputStream in = Thread.currentThread().getContextClassLoader().getResourceAsStream("dao.properties");
            Properties prop = new Properties();
            prop.load(in);
            String className = prop.getProperty("cn.bean.user.dao.UserDao");
            Class clazz = Class.forName(className);
            userDao = (UserDao) clazz.newInstance();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
 
    public static UserDao getUserDao() {
        return userDao;
    }
}
```

## 时间类型的转换

**为什么需要进行时间类型的转换？**

- ResultSet#getDate() 返回的是 java.sql.Date
- 领域对象 (Domain) 中的所有属性不能出现 java.sql 包下的东西
- 所以要进行 java.util.Date 与 java.sql.Date、Time、Timestamp 之间的转换

**SQL中时间相关的类：**

- `java.sql.Date`：表示日期，只有年月日，没有时分秒，会丢失时间
- `java.sql.Time`：表示时间，只有时分秒，没有年月日，会丢失日期
- `java.sql.Timestamp`：表示时间戳，有年月日时分秒，以及毫秒

这三个类都是`java.util.Date`的子类。

**java.sql到java.util**

sql 的三个时间类型都是 java.util.Date 的子类，把子类对象给父类引用不需要转换。

**java.util到java.sql**

当需要把 java.util.Date 转换成 sql 的三种时间类型时，先通过 java.util.Date 的 getTime() 方法获取毫秒值，再通过毫秒值构造 sql 时间相关的对象即可，例如：

```java
java.util.Date d = new java.util.Date();
java.sql.Date date = new java.sql.Date(d.getTime());
Time time = new Time(d.getTime());
Timestamp timestamp = new Timestamp(d.getTime());
```

## 在数据库中存储大数据

**目标：**保存一个 mp3 文件到数据库中。

**注意：**需要在数据库的 my.ini 配置文件中添加一行：`max_allowed_packet=10485760`。

对于一个 mp3 文件，采用 mediumblob (16M) 就够用了。

**步骤：**

先创建一张表：

```sql
CREATE TABLE big_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    filename VARCHAR(100),
    data MEDIUMBLOB
);
```

**Store：**

```java
public void dbStore() {
    Connection con = null;
    PreparedStatement pstmt = null;
    try {
        con = JDBCUtils.getConnection();
        String sql = "INSERT INTO big_data VALUES(?, ?, ?)";
        pstmt = con.prepareStatement(sql);
        pstmt.setInt(1, 1);
        pstmt.setString(2, "风衣");
        InputStream mp3 = new FileInputStream("C:/Users/Bean/Music/风衣.mp3");
        pstmt.setBinaryStream(3, mp3);  // 存到数据库
        pstmt.executeUpdate();
    } catch (SQLException e) {
        throw new RuntimeException(e);
    } catch (IOException e) {
        throw new RuntimeException(e);
    } finally {
        try {
            if (pstmt != null) {
                pstmt.close();
            } else if (con != null) {
                con.close();
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }
}
```

**Load：**

```java
public void dbLoad() {
    Connection con = null;
    PreparedStatement pstmt = null;
    ResultSet res = null;
    try {
        con = JDBCUtils.getConnection();
        String sql = "select `data` from big_data where filename=?";
        pstmt = con.prepareStatement(sql);
        String filename = "风衣";
        pstmt.setString(1, filename);
        res = pstmt.executeQuery();
        res.next();
        InputStream in = res.getBinaryStream("data");  // 从结果集中取出数据
        OutputStream out = new FileOutputStream("C:/Users/Bean/Documents/" + filename + ".mp3");
        org.apache.commons.io.IOUtils.copy(in, out);
        System.out.println("Finish.");
    } catch (SQLException e) {
        throw new RuntimeException(e);
    } catch (IOException e) {
        throw new RuntimeException(e);
    }
}
```

还有一种方法，就是把要存储的数据包装成 Blob 类型，然后调用 PreparedStatement 的 setBlob() 方法来设置数据，getBlob 方法取出数据。代码示例如下：

**Store：**

```java
con = JdbcUtils.getConnection();
String sql = "insert into tab_bin(filename,data) values(?, ?)";
pstmt = con.prepareStatement(sql);
pstmt.setString(1, "a.jpg");
// 开始存了！
File file = new File("f:\\a.jpg");
byte[] datas = FileUtils.getBytes(file);  // 获取文件中的数据
Blob blob = new SerialBlob(datas);  // 创建Blob对象，Blob是个接口，要用它的实现类SerialBlob(byte[] data)
pstmt.setBlob(2, blob);  // 设置Blob类型的参数
pstmt.executeUpdate();
```

**Load：**

```java
con = JdbcUtils.getConnection();
String sql = "select filename,data from tab_bin where id=?";
pstmt = con.prepareStatement(sql);
pstmt.setInt(1, 1);
rs = pstmt.executeQuery();
rs.next();
String filename = rs.getString("filename");
// 开始取了！
File file = new File("F:\\" + filename) ;
Blob blob = rs.getBlob("data");
byte[] datas = blob.getBytes(0, (int)file.length());
FileUtils.writeByteArrayToFile(file, datas);
```

## 批处理

批处理就是一批一批的处理，而不是一个一个的。即一次向服务器发送多条SQL语句，然后由服务器一次性处理。注意：批处理只针对更新 (增、删、改) 语句，批处理没有查询什么事儿！

**Statement：**

- `void addBatch(String sql)`：添加一条语句到"批"中
- `int[] executeBatch()`：执行"批"中的每一条语句，并返回每一条语句影响的行数
- `void clearBatch()`：清空"批"中的语句

```java
for (int i = 0; i < 10; i++) {
    String number = "S_10" + i;
    String name = "stu" + i;
    int age = 20 + i;
    String gender = i % 2 == 0 ? "male" : "female";
    String sql = "insert into stu values('" + number + "', '" + name + "', " + age + ", '" + gender + "')";
    stmt.addBatch(sql);
}
stmt.executeBatch();
```

**PreparedStatement：**

```java
Strint sql = "insert into stu values(?, ?, ?, ?)";
pstmt = con.preparedStatement(sql);
for (int i = 0; i < 10; i++) {
    pstmt.setString(1, "S_10" + i);
    pstmt.setString(2, "stu" + i);
    pstmt.setInt(3, 20 + i);
    pstmt.setString(4, i % 2 == 0 ? "male" : "female");
    pstmt.addBatch();
}
pstmt.executeBatch();
```