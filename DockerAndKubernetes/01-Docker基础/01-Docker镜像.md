# Docker 镜像

Docker 的镜像是一个只读模板，我们可以通过这个模板来创建容器，也就是说，镜像是创建 Docker 容器的基础。

通过版本管理和增量的文件系统，Docker 提供了一套十分简单的机制来创建和更新现有的镜像。

<!-- TOC -->

- [Docker 镜像](#docker-%E9%95%9C%E5%83%8F)
  - [使用别人的 image](#%E4%BD%BF%E7%94%A8%E5%88%AB%E4%BA%BA%E7%9A%84-image)
    - [从 DockerHub 上搜索 image](#%E4%BB%8E-dockerhub-%E4%B8%8A%E6%90%9C%E7%B4%A2-image)
    - [获取别人的 image](#%E8%8E%B7%E5%8F%96%E5%88%AB%E4%BA%BA%E7%9A%84-image)
    - [查看 image 信息](#%E6%9F%A5%E7%9C%8B-image-%E4%BF%A1%E6%81%AF)
    - [删除 & 清理 image](#%E5%88%A0%E9%99%A4--%E6%B8%85%E7%90%86-image)
  - [创建自己的 image](#%E5%88%9B%E5%BB%BA%E8%87%AA%E5%B7%B1%E7%9A%84-image)
    - [创建 image 的三种方式](#%E5%88%9B%E5%BB%BA-image-%E7%9A%84%E4%B8%89%E7%A7%8D%E6%96%B9%E5%BC%8F)
    - [将 image 存成 .tar 本地文件及其其逆过程](#%E5%B0%86-image-%E5%AD%98%E6%88%90-tar-%E6%9C%AC%E5%9C%B0%E6%96%87%E4%BB%B6%E5%8F%8A%E5%85%B6%E5%85%B6%E9%80%86%E8%BF%87%E7%A8%8B)
    - [发布镜像](#%E5%8F%91%E5%B8%83%E9%95%9C%E5%83%8F)

<!-- /TOC -->

## 使用别人的 image

### 从 DockerHub 上搜索 image

命令：`docker search`

例子：

```shell
docker search --filter=is-official=true nginx  # 搜索官方镜像
docker search --filter=stars=4 tensorflow  # 搜索 star 数超过 4 的
```

### 获取别人的 image

命令：`docker pull`

例子：

```shell
docker pull ubuntu  # 不显式指定 :TAG，或默认选择 latest 标签
# 可以使用 tag 命令为本地的镜像添加标签
docker tag ubuntu:latest myubuntu:latest
```

从下载的过程就可以看出，镜像文件一般由若干层组成，它是一层一层的下载的。

### 查看 image 信息

命令：

- `docker images`：列出本地主机上已有的镜像信息；
- `docker inspect`：获取镜像的详细信息，包括制作者、适应架构、各层的数字摘要等；
- `docker history`：查看镜像的创建过程。

### 删除 & 清理 image

命令：

- `docker rmi`：当通过 `镜像名:TAG` 来删除时，删除的是镜像多个标签中的一个，如果这个镜像只剩下一个标签了，那么会彻底删除这个镜像；
- `docker image prune`：清理没有被使用的镜像。

例子：

```shell
docker image prune -f
```



## 创建自己的 image

### 创建 image 的三种方式

命令：

- `docker commit`：基于已有的镜像容器创建；
- `docker import`：基于本地模板导入；
- `docker build`：基于 Dockersfile 创建。

### 将 image 存成 .tar 本地文件及其其逆过程

命令：

- `docker save`：导出镜像到本地 .tar 文件；
- `docker load`：将导出的 .tar 文件再导入本地镜像库。

例子：

```shell
# save
docker save -o ubuntu_18.04.tar ubuntu:18.04
# load
docker load -i ubuntu_18.04.tar
docker load < ubuntu_18.04.tar
```

### 发布镜像

命令：`docker push`