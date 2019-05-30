# Docker 镜像

Docker 的镜像是一个只读模板，我们可以通过这个模板来创建容器，也就是说，镜像是创建 Docker 容器的基础。

通过版本管理和增量的文件系统，Docker 提供了一套十分简单的机制来创建和更新现有的镜像。



## Docker 镜像概述

Docker 镜像由多个层组成，每层叠加之后，从外部看起来就是一个独立的对象。镜像内部是一个精简的操作系统，同时还包含应用运行所必须的文件和依赖包。

镜像相当于是一个创建容器的模板，一旦容器从镜像启动以后，二者之间就变成了相互依存的关系，并且在镜像上启动的容器全部停止之前，镜像是无法被删除的。



## 使用别人的 image

### 从 DockerHub 上搜索 image

**命令：** `docker search`

**例子：**

```shell
docker search --filter=is-official=true nginx  # 搜索官方镜像
docker search --filter=stars=4 tensorflow  # 搜索 star 数超过 4 的
```

### 获取别人的 image

**命令：** `docker pull`，Linux Docker 主机本地镜像仓库通常位于 `/var/lib/docker/<storage-driver>`。

**例子：**

```shell
docker pull ubuntu  # 不显式指定 :TAG，或默认选择 latest 标签
# 可以使用 tag 命令为本地的镜像添加标签
docker tag ubuntu:latest myubuntu:latest
```

**注意：**

- 从下载的过程就可以看出，镜像文件一般由若干层组成，它是一层一层的下载的；

- 在拉取镜像时，不要认为 latest 一定是仓库中的最新镜像，例如，Alpine 仓库中的最新镜像通常是 edge；

- 从非官方仓库拉取镜像时，需要在仓库名称前面机上 Docker Hub 的用户名或者组织名。

	```shell
	docker image pull microsoft/powershell:nanoserver
	```

> **多架构镜像：**
>
> Docker 的镜像仓库是支持多架构镜像的，也就是说，某个镜像仓库标签下的镜像（repository:tag）可以同时支持 64 位 Linux、PowerPC Linux、64 位 Windows 和 ARM 等多种架构，简单来说就是：**一个镜像标签之下可以支持多个平台和架构。**
>
> **多架构镜像的实现：**
>
> 镜像仓库服务 API 支持两种重要的结构：Manifest 列表和 Manifest。
>
> Manifest 列表列出了一个镜像标签所支持的架构，列表中的每一项都指向一个具体的 Manifest，Manifest 种包含了镜像配置和镜像层信息。
>
> 在拉取镜像时，如果该镜像有 Manifest 列表，Docker Client 会找到所需架构对应的 Manifest 并解析出组成该镜像的镜像层加密 ID，然后根据 ID 从 Docker Hub 二进制存储种拉去每个镜像层。

### 查看 image 信息

**命令：**

- `docker images`：列出本地主机上已有的镜像信息；

	- 可以使用 `--filter` 来过滤返回的镜像信息

		```shell
		docker images --filter dangling=true
		```

- `docker inspect`：获取镜像的详细信息，包括制作者、适应架构、各层的数字摘要等；

- `docker history`：查看镜像的创建过程。

### 删除 & 清理 image

**命令：**

- `docker rmi`：当通过 `镜像名:TAG` 来删除时，删除的是镜像多个标签中的一个，如果这个镜像只剩下一个标签了，那么会彻底删除这个镜像；
- `docker image prune`：清理没有被使用的镜像。

**例子：**

```shell
docker image prune -f
```

> **虚悬镜像：`<none>:<none>`**
>
> 在构建一个新的镜像时，如果为新的镜像打了一个已经存在的 tag，那么 Docker 会移除旧镜像上的标签，将该标签标在新的镜像上，旧的镜像会变成一个 “虚悬镜像”，也就是 `<none>:<none>` 镜像。
>
> 可以通过 `dangling=true` 来判断一个镜像是不是虚悬镜像。



## 创建自己的 image

### 创建 image 的三种方式

**命令：**

- `docker commit`：基于已有的镜像容器创建；
- `docker import`：基于本地模板导入；
- `docker build`：基于 Dockersfile 创建。

### 将 image 存成 .tar 本地文件及其其逆过程

**命令：**

- `docker save`：导出镜像到本地 .tar 文件；
- `docker load`：将导出的 .tar 文件再导入本地镜像库。

**例子：**

```shell
# save
docker save -o ubuntu_18.04.tar ubuntu:18.04
# load
docker load -i ubuntu_18.04.tar
docker load < ubuntu_18.04.tar
```

### 发布镜像

**命令：** `docker push`

