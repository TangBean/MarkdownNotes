# Python 开发和调试运行在虚拟机 Docker 中的项目

> **Reference:**
>
> - https://www.cnblogs.com/jackadam/p/8976873.html

开始的开始，我们需要一个安装了 Dokcer 的 Linux 虚拟机，并且是一个固定 IP 的虚拟机。



创建一个 Dockerfile：

```dockerfile
from alpine:3.9
MAINTAINER Tang_Bean<tang_bean@163.com>
# 变更源, 设置默认时区为亚洲/上海
RUN { \
        echo 'http://mirrors.ustc.edu.cn/alpine/v3.7/main'; \
        echo 'http://mirrors.ustc.edu.cn/alpine/v3.7/community'; \
        echo 'http://mirrors.ustc.edu.cn/alpine/edge/main'; \
        echo 'http://mirrors.ustc.edu.cn/alpine/edge/community'; \
        echo 'http://mirrors.ustc.edu.cn/alpine/edge/testing'; \
    } > /etc/apk/repositories && \
    apk add --no-cache --upgrade apk-tools openssh tzdata && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    apk del tzdata
# 修改 root 密码
RUN echo root:123456 | chpasswd
# 生成 KEY
RUN ssh-keygen -q -t rsa -b 2048 -f /etc/ssh/ssh_host_rsa_key -P '' -N ''
# 允许远程登录
RUN sed -i "s/#PermitRootLogin.*/PermitRootLogin yes/g" /etc/ssh/sshd_config
# 开放22端口
EXPOSE 22

# 增加python3
RUN echo "**** install Python ****" && \
    apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    apk add sudo

CMD /usr/sbin/sshd -D
```



然后 build 镜像并创建一个容器：

```shell
$ docker build -t ssh .
$ docker run -d -t --restart=always --privileged --name ssh -p 2222:22  ssh
```



然后就可以了，可以去 PyCharm 中连接了。

剩下的参考那篇文章就可以了。