# 使用 Docker 快速搭建 Kafka 开发环境

> **Reference：**
>
> - https://tomoyadeng.github.io/blog/2018/06/02/kafka-cluster-in-docker/index.html

因为根本不想啥都搞个 windows 版的，所以 Vagrant 起虚拟机上 Docker 吧！

所以本文的

首先，先把虚拟机的 Python 版本从 3.5 改到 3.6 去：

```shell
$ sudo update-alternatives --install /usr/bin/python python3 /usr/bin/python3.6 1
update-alternatives: using /usr/bin/python3.6 to provide /usr/bin/python (python3) in auto mode
```

