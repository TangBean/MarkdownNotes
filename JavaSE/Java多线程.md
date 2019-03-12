# Java 多线程



## 关于 synchronized 关键字的 5 连击

### 说一说自己对于 synchronized 关键字的了解



### synchronized 关键字的使用

- 修饰实例方法，作用于当前对象实例加锁，进入同步代码前要获得当前对象实例的锁。
- 修饰静态方法，作用于当前类对象加锁，进入同步代码前要获得当前类对象的锁。
- 修饰代码块，指定加锁对象，对给定对象加锁，进入同步代码库前要获得给定对象的锁。

由于修饰实例方法和静态方法时的加锁对象是不同的，所以如果一个线程 A 调用一个实例对象的非静态 synchronized 方法，而线程 B 需要调用这个实例对象所属类的静态 synchronized 方法，是允许的，不会发生互斥现象。

虽然双重检验锁方式实现单例模式并不被推荐，不过倒是很喜欢用它来考 synchronized……，下面是实现方式：

```java
public class Singleton {
    private volatile static Singleton instance;
    private Singleton() {}
    
    public static Singleton getInstance() {
        // 先判断对象是否已经实例过，没有实例化过才进入加锁代码
        // 相当于通过缩小加锁的范围来提高性能
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

### synchronized 关键字的底层原理

我们通过下面这段代码的反编译结果来研究 synchronized 关键字的底层原理。

```java
public class SynchronizedDemo {
    public void method() {
        synchronized (this) {
            System.out.println("synchronized");
        }
    }
}
```

通过 `javap -c -s -v -l SynchronizedDemo.class` 反编译这段代码，得到：

```java
public void method();
  descriptor: ()V
  flags: ACC_PUBLIC
  Code:
    stack=2, locals=3, args_size=1
       0: aload_0
       1: dup
       2: astore_1
       3: monitorenter // 加锁！
       4: getstatic     #2                  // Field java/lang/System.out:Ljava/io/PrintStream;
       7: ldc           #3                  // String synchronized
       9: invokevirtual #4                  // Method java/io/PrintStream.println:(Ljava/lang/String;)V 
      12: aload_1
      13: monitorexit // 放锁！
      14: goto          22
      17: astore_2
      18: aload_1
      19: monitorexit
      20: aload_2
      21: athrow
      22: return
```

JVM 是基于进入和退出 monitor 对象来实现方法同步和代码块同步的。代码块的同步是通过 `monitorenter` 和 `monitorexit` 实现的，方法同步使用的是另一种方式，细节在 JVM 规范中并没有详细说明。

当一个线程执行到 `monitorenter` 指令时，会尝试获取对象对应的 monitor 的所有权，任何对象都有一个 monitor 与之关联，当一个 monitor 被持有后，该对象所保护的区域将处于锁定状态，因为其他线程这时不能持有 monitor。这个 monitor 保存在 Java对象的对象头中。

### JDK1.6 之后的 synchronized 关键字底层做了哪些优化

JDK1.6 对锁的实现引入了大量的优化，如偏向锁、轻量级锁、自旋锁、适应性自旋锁、锁消除、锁粗化等技术来减少锁操作的开销。

锁主要存在四种状态，依次是：无锁状态、偏向锁状态、轻量级锁状态、重量级锁状态，他们会随着竞争的激烈而逐渐升级。注意锁可以升级不可降级，这种策略是为了提高获得锁和释放锁的效率。

### synchronized 和 ReenTrantLock 的区别

- **都是可重入锁**
	- 即自己拿到锁之后可以再次获取自己内部的锁，如果不能可重入锁的话，就会发生死锁。可重入锁可以通过为每个锁关联一个获取该锁的次数的计数器 count，和一个所有者线程来实现，同一个线程每获取一次锁，锁的计数器都 +1，每放开一次锁，锁的计数器都加 -1，等到锁的计数器减为 0，表明这个线程放开了这个锁。
- **synchronized 依赖于 JVM，ReenTrantLock 依赖于 API**
- **ReentrantLock 有如下高级功能：**
	- 可轮询、可定时、可中断的锁
	- 公平锁
	- 非块结构的锁
	- 可实现选择性通知

在不需要 ReentrantLock 提供的高级功能时，优先选择 synchronized，**原因如下：**

- Java 6 开始，ReenstrantLock 和内置锁的性能相差不大；
- synchronized 是 JVM 的内置属性，未来更有可能对 synchronized 进行性能优化，如对线程封闭的锁对象的锁消除，增加锁的粒度等；
- ReenstrantLock 危险性更高（如忘记在 finally 块中 lock.unlock() 了，会导致锁永远无法被释放，出现问题，极难 debug）；
- 许多现有程序中已使用了 synchronized，两种方式混合使用比较易错。



## 关于 volatile 的 2 连击





## 关于线程池的 4 连击

### 为什么要用线程池？



### 实现 Runnable 接口和 Callable 接口的区别？



### 执行 execute() 方法和 submit() 方法的区别？



### 如何创建线程池





## 关于 Atomic 原子类的 4 连击

### 介绍一下 Atomic 原子类



### JUC 包中的原子类是哪 4 类?



### 讲讲 AtomicInteger 的使用



### 简单介绍一下 AtomicInteger 类的原理





## AQS

### AQS 介绍



### AQS 原理分析



### AQS 组件总结





## 线程状态





## 线程通信方式





## 中断线程





## 死锁





## 非阻塞同步机制







