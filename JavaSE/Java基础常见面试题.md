# Java 基础常见面试题



## 面向对象和面向过程的区别？

面向过程是编年体，面向对象是纪传体。

- **面向过程：** 分析出解决问题所需要的步骤，然后用函数把这些步骤一步一步实现，使用的时候一个一个依次调用就可以了。
- **面向对象：** 把构成问题事物分解成各个对象，建立对象的目的不是为了完成一个步骤，而是为了描叙某个事物在整个解决问题的步骤中的行为。

例如设计一个五子棋游戏：

面向过程的设计思路是，首先分析问题的步骤：1、开始游戏，2、黑子先走，3、绘制画面，4、判断输赢，5、轮到白子，6、绘制画面，7、判断输赢，8、返回步骤2，9、输出最后结果。把上面每个步骤用分别的函数来实现，问题就解决了。 

面向对象的设计思路是，将整个五子棋分为：1、黑白双方，2、棋盘系统，负责绘制画面，3、规则系统，负责判定诸如犯规、输赢等。第一类对象（玩家对象）负责接受用户输入，并告知第二类对象（棋盘对象）棋子布局的变化，棋盘对象接收到了棋子的变化就要负责在屏幕上面显示出这种变化，同时利用第三类对象（规则系统）来对棋局进行判定。



## Java 的三个基本特性，在项目中那些地方用到多态

- **封装：** 要求低耦合高内聚，可以说，封装就是隐藏一切可隐藏的东西，只向外界提供最简单的编程接口。
- **继承：** 继承是通过已有的类（父类）创建新类（子类）的过程，这让软件系统有了一定的延续性。
- **多态：** 允许不同的子类对象对同一消息做出不同的响应。
	- 实现：1. 方法重写，2. 用父类型引用子类型，然后调用重写了的方法。

代理模式用到了多态。



## 方法的重载和重写

首先，它们的共同点就是 **方法名一定要相同** ！区别在于：

- **重载：** 发生在同一个类中，参数必须不同（类型 or 个数 or 顺序，不包括返回参数），方法返回值和访问修饰符可以不同，发生在编译时。
- **重写：** 发生在父子类中，参数列表必须相同，返回值范围和抛出的异常范围小于等于父类，访问修饰符范围大于等于父类（如果父类方法访问修饰符为 private 则子类就不能重写该方法），发生在运行时。

除此之外，重载与重写的实现方式也很不一样，它们的区别在于方法分派上，方法分派就是在方法调用前，确定要调用的方法到底是哪一个，它的实际入口地址到底在哪，而 **重载是基于方法的静态分派实现的，重写是基于方法的动态分派实现的** 。

那么什么是方法的静态分派和动态分派呢？[详见这里](https://github.com/TangBean/understanding-the-jvm/blob/master/Ch2-Java%E8%99%9A%E6%8B%9F%E6%9C%BA%E7%A8%8B%E5%BA%8F%E6%89%A7%E8%A1%8C/02-%E8%99%9A%E6%8B%9F%E6%9C%BA%E5%AD%97%E8%8A%82%E7%A0%81%E6%89%A7%E8%A1%8C%E5%BC%95%E6%93%8E_01-%E6%96%B9%E6%B3%95%E8%B0%83%E7%94%A8.md#%E5%88%86%E6%B4%BE%E8%B0%83%E7%94%A8)。

为了不影响阅读，在这里再简单总结下：

- 静态分派：编译时，通过方法的参数（类型 & 个数 & 顺序）这种静态的东西来判断到底调用哪个方法。
- 动态分派：运行时，通过方法的接收者这种动态的东西来判断到底调用哪个方法。

通过以上两条，我们也能得出为什么重载是基于方法的静态分派实现的，重写是基于方法的动态分派实现的了。



## 自动装箱与拆箱

- **装箱：** 将基本类型用它们对应的引用类型包装起来；
- **拆箱：** 将包装类型转换为基本数据类型；



## `==` 与 `equals`

- **`==`：** 判断两个对象的地址是不是相等。
	- 两个操作数都是包装类的引用时，比较的是是否为同一个对象；
	- **当其中有一个参数包含算术运算时，会触发自动拆箱，比较的是数值**，并且可以进行如 int 和 long 之间的转型比较操作；
	- 但不遇算术运算不会自动拆箱；
- **`equals`：** 
	- 会自动拆箱；
	- **不会处理如 int 和 long 之间的转型比较问题**，比如 `int a = 1` 和 `long b = 1L` 进行比较 `a == b`，会因为类型不同而直接返回 false，但是用 `==` 比较的话就会返回 true。

看一段几乎包含了所有判等情况的代码：

```java
public static void main(String[] args) {
    Integer a = 1;
    Integer b = 2;
    Integer c = 3;
    Integer d = 3;
    Integer e = 321;
    Integer f = 321;
    Long g = 3L;
    Double gg = 3.0;
    System.out.println("Integer");
    System.out.println(c == d);             // true
    System.out.println(e == f);             // false
    System.out.println(c == (a + b));       // true
    System.out.println(c.equals(a + b));    // true
    System.out.println(g == (a + b));       // true
    System.out.println(g.equals(a + b));    // false
    System.out.println(gg.equals(a + b));   // false

    System.out.println("Boolean");
    Boolean h = true;
    Boolean i = true;
    System.out.println(h == i);  // true

    System.out.println("Double");
    Double j = 1.0;
    Double k = 1.0;
    System.out.println(j == k);         // false
    System.out.println(j.equals(k));    // true
}
```



## 接口和抽象类的区别

1. 接口的方法默认是 public，所有方法在接口中不能有实现（Java 8 开始接口方法可以有默认实现），抽象类可以有非抽象的方法；
2. 接口中的实例变量默认是 final 类型的，而抽象类中则不一定；
3. 一个类可以实现多个接口，但最多只能实现一个抽象类；
4. 一个类实现接口的话要实现接口的所有方法，而抽象类不一定；
5. 接口不能用 new 实例化，但可以声明，但是必须引用一个实现该接口的对象；
6. 从设计层面来说，抽象是对类的抽象，是一种模板设计，接口是行为的抽象，是一种行为的规范。

> 补充：在 JDK8 中，接口也可以定义静态方法，可以直接用接口名调用。**实现类是不可以调用的。如果同时实现两个接口，接口中定义了一样的默认方法，必须重写，不然会报错。**



## static 和 final 的区别和用途

### static

- **修饰变量：** 静态变量随着类加载时被完成初始化，内存中只有一个，且 JVM 也只会为它分配一次内存，该类的所有实例共享静态变量。
- **修饰方法：** 在类加载的时候就存在，不依赖任何实例；static 方法必须实现，不能用 abstract 修饰。
- **修饰代码块：** 在类加载过程中的初始化阶段会执行静态代码块中的内容，静态代码中的内容会和 static 变量的赋值操作一起被组合到 `<client>()` 方法中，并在初始化阶段被执行。
- **执行顺序：** 父类静态代码块 -> 子类静态代码块 -> 父类非静态代码块 -> 父类构造方法 -> 子类非静态代码块 -> 子类构造方法

### final

- **修饰变量：**
  - 基本数据类型的变量：数值一旦在初始化之后便不能更改。
  - 引用类型的变量：在对其初始化之后便不能再让其指向另一个对象，但引用的对象内容可变。
- **修饰方法：** 不能被继承，不能被子类修改。
	- 使用 final 方法的原因：
		- 把方法锁定，以防任何继承类修改它的含义；
		- final 方法效率高，因为在早期的Java实现版本中，会将 final 方法转为内嵌调用，这样就节省了方法调用的开销。但是如果方法过于庞大，可能看不到内嵌调用带来的任何性能提升（现在的 Java 版本已经不需要使用 final 方法进行这些优化了）。类中所有的 private 方法都隐式地指定为 final。
- **修饰类：** 不能被继承，final 类中的所有成员方法都会被隐式地指定为final方法。
- **修饰形参：** final 形参不可变。

final 一定程度上可以用来防止指令的重排序，比如：

```java
public class Holder {
    private int n;
    // private final int n; // 这句可以解决这个问题

    public Holder(int n) {
        // 一个线程执行到这，另一个线程进来了，这时候虽然对象还没有构造好，但另一个线程已经拿到对象了
        this.n = n;
    }

    public void assertSanity() {
        // 会成立原因：某个线程在n != n时，第一次读取到 n 是一个失效值，
        // 第二次读取到的是更新后的值，就抛异常了。
        if (n != n) { 
            throw new AssertionError("n != n");
        }
    }
}
```

这个问题发生的主要原因就是对对象初始引用的调用被重排序排到了构造函数前面，用了 final 修饰需要在构造函数中修饰的变量可以解决这个问题，因为：

- 对于含有 final 域的对象，JVM 必须保证对象的初始引用在构造函数之后执行，不能乱序执行；
- 也就是说，一旦得到了对象的引用，那么这个对象的 final 域一定是已经完成了初始化的。



## Object 类的常见方法总结

```java
// native方法，用于返回当前运行时对象的Class对象，使用了final关键字修饰，故不允许子类重写。
public final native Class<?> getClass();

// native方法，用于返回对象的哈希码，主要使用在哈希表中，比如JDK中的HashMap。
public native int hashCode();

// naitive方法，用于创建并返回当前对象的一份拷贝。
// 一般情况下，对于任何对象 x，表达式 x.clone() != x 为true，x.clone().getClass() == x.getClass() 为true。
// Object本身没有实现Cloneable接口，所以不重写clone方法并且进行调用的话会发生CloneNotSupportedException异常。
protected native Object clone() throws CloneNotSupportedException;

// 用于比较2个对象的内存地址是否相等，String类对该方法进行了重写用户比较字符串的值是否相等。
public boolean equals(Object obj);

// 返回类的名字@实例的哈希码的16进制的字符串。建议Object所有的子类都重写这个方法。
public String toString();

// native方法，并且不能重写。唤醒一个在此对象监视器上等待的线程(监视器相当于就是锁的概念)。
// 如果有多个线程在等待只会任意唤醒一个。
public final native void notify();

// native方法，并且不能重写。跟notify一样，唯一的区别就是会唤醒在此对象监视器上等待的所有线程，而不是一个线程。
public final native void notifyAll();

// native方法，并且不能重写。暂停线程的执行。注意：sleep方法没有释放锁，而wait方法释放了锁 。timeout是等待时间。
public final native void wait(long timeout) throws InterruptedException;

// 多了nanos参数，这个参数表示额外时间（以毫微秒为单位，范围是 0-999999）。 所以超时的时间还需要加上nanos毫秒。
public final void wait(long timeout, int nanos) throws InterruptedException;

// 跟之前的2个wait方法一样，只不过该方法一直等待，没有超时时间这个概念
public final void wait() throws InterruptedException;

// 实例被垃圾回收器回收的时候触发的操作，它能干的finally块都能干，所以不要用，因为虚拟机并不保证这个方法执行完成
protected void finalize() throws Throwable { }
```



## String、StringBuffer、StringBuilder 以及对 String 不变性的理解

### 可变性

简单的来说：String 类中使用 final 关键字字符数组保存字符串，`private final char value[]`，所以 String 对象是不可变的。而 StringBuilder 与 StringBuffer 都继承自 AbstractStringBuilder 类，在 AbstractStringBuilder 中也是使用字符数组保存字符串 `char[] value` 但是没有用 final 关键字修饰，所以这两种对象都是可变的。

```java
abstract class AbstractStringBuilder implements Appendable, CharSequence {
    char[] value; // 无 final 修饰
    int count;
    AbstractStringBuilder() {
    }
    AbstractStringBuilder(int capacity) {
    	value = new char[capacity];
    }
    ...
}
```

### 线程安全性

String 中的对象是不可变的，也就可以理解为常量，线程安全。

AbstractStringBuilder 是 StringBuilder 与StringBuffer 的公共父类，定义了一些字符串的基本操作，如 expandCapacity、append、insert、indexOf 等公共方法。不过 StringBuffer 对方法加了同步锁或者对调用的方法加了同步锁，所以是线程安全的。StringBuilder 并没有对方法进行加同步锁，所以是非线程安全的。

### 性能

每次对 String 类型进行改变的时候，都会生成一个新的 String 对象，然后将指针指向新的 String 对象。StringBuffer 每次都会对 StringBuffer 对象本身进行操作，而不是生成新的对象并改变对象引用。相同情况下使用 StirngBuilder 相比使用 StringBuffer 仅能获得 10%~15% 左右的性能提升，但却要冒多线程不安全的风险。

### 对于三者使用的总结

- 操作少量的数据 —— String
- 单线程操作字符串缓冲区下操作大量数据 —— StringBuilder
- 多线程操作字符串缓冲区下操作大量数据 —— StringBuffer

### String 不变性的理解

- String 类是 final 的，不能被继承，我们是不能继承它改造它的。
- 使用 “+” 连接字符串时不是在原有的字符串上进行修改，而是创建新的字符串。
- 在 Java 中，通过使用 “+” 符号来串联字符串的时候，实际上底层会转成通过 StringBuilder 实例的 append() 方法来实现。
- `String s = new String("Hello world");` 可能创建两个对象也可能创建一个对象。如果静态区中有 "Hello world" 字符串常对象的话，则仅仅在堆中创建一个对象。如果静态区中没有 "Hello world" 对象，则堆上和静态区中都需要创建对象。

### String 有重写 Obiect 的 hashCode 和 toString 吗？

- String 重写了 Object 类的 hashCode 和 toString 方法。
- 如果重写 equals 一定要重写 hashCode，因为有如下几个规定需要遵守：
	- `o1.equals(o2) == true`，则 `o1.hashCode() == o2.hashCode()` 一定为 true
	- `o1.hashCode() == o2.hashCode()` 为 false 时，`o1.equals(o2) == false`
	- `o1.hashCode() == o2.hashCode()` 为 true 时，`o1.equals(o2)` 不一定为 true
- 如果重写 equals 但不重写 hashCode ，在比如用 HashSet 时，如果 `原对象.equals(新对象)`，但没有重写 hashCode，那么集合中会存在两个值相同的对象。



## Java 序列化

### 如何实现序列化和反序列化



### 常见的序列化协议





## Java 多线程的三种方式及其区别







## 什么是线程安全







## 多线程如何进行信息交互







## 多线程共用一个数据变量需要注意什么？







## 线程池

### 什么是线程池？



### 如果让你设计一个动态大小的线程池，如何设计，有哪些方法？





## Java 是否有内存泄露和内存溢出的风险







## 异常

### 常见异常分为哪两种

Exception 和 Error。

### 常见异常的基类以及常见的异常





## Java 中的 NIO，BIO，AIO 分别是什么？







## 匿名内部类是什么？如何访问在其外面定义的变量？







## 泛型







## Java 枚举类







## Java 反射







## Java 动态代理







## 为什么要实现内存模型？



