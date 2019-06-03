# Docker 数据卷

容器中的数据管理方式主要有以下两种：

- 数据卷：容器内的数据直接映射到主机环境；
- 数据卷容器：一个有数据卷的容器，用来提供数据卷给其他容器挂载。



## 数据卷

### 什么是数据卷

数据卷就是主机中的一个特殊目录，这个目录可以提供给容器使用。用户创建卷，然后创建容器，接着将卷挂载到容器文件系统的某个目录之下，任何写到该目录下的内容都会写到卷中，即使容器被删除，卷与其上面的数据依然存在，容器与卷是一个非耦合的关系。这个行为类似于 LInux 的 mount，其实就是将主机中的目录直接映射进容器。（感觉容器就像一台电脑，卷就像一个移动硬盘）

> **mount 的原理**

### 数据卷的特性

- 数据卷可以在容器之间共享和重用，可以被用来在容器间传递数据；
- 无论是容器内操作还是本地主机的操作，对数据卷内数据的修改会立即生效；
- 对数据卷的更新不会影响到镜像，可以将应用与数据解耦；
- 数据卷会一直存在，即便没有容器使用它，如果一个数据卷没有被容器使用时，我们可以安全的把它删掉。

### docker volume 常用命令

- `docker volume create`：创建新卷，在 Linux 系统中，创建的卷放在 `/var/lib/docker/<storage-driver>/` 下

	```shell
	docker volume create myvol
	```

- `docker volume ls`：列出本地 Docker 主机上的所有卷

- `docker volume inspect`：查看卷的详细信息，可以用来查看卷在 Docker 主机文件系统中的位置

- `docker volume prune`：删除未被容器或者服务副本使用的全部卷，谨慎使用

- `docker volume rm`：删除未被使用的卷

### 挂载数据卷

除了使用 `volume` 子命令来管理数据卷以外，我们还可以将本地主机的任意目录挂载到容器内作为数据卷，这种数据卷叫 “绑定数据卷”，此外，还有一种只存在于内存中的 “临时数据卷”。

我们可以在使用 `docker run` 命令时，通过 `--mount` 选项来为容器挂载数据卷，`--mount` 支持 3 中类型的数据卷：

- `type=volume`：普通数据卷，映射到主机的 `/var/lib/docker/volumes` 路径下；
- `type=bind`：绑定数据卷，映射到主机的指定目录下；
- `type=tmpfs`：临时数据卷，只存在于内存中。

挂载时，通过 `source` 和 `target` 指定需要被挂载的数据卷和挂载在容器中的位置：

```shell
$ docker run -dit --name voltainer \
  --mount source=myvol,target=/vol \
  aipine
```

此时，如果系统中存在 myvol 卷，会挂载该卷，如果不存在，则会创建 myvol 卷。

也可以将 Docker 主机中的一个目录挂载进容器中：

```shell
$ docker run -dit --name voltainer \
  --mount type=bind,source=/mydir,target=/vol \
  aipine 
```

此外，我们还可以通过 `-v` 选项来为容器创建数据卷：

```shell
$ docker run -dit --name voltainer \
  -v /mydir:/vol:ro \  # 默认是 rw，既读写，这里使用 ro 修改为只读的
  aipine 
```

也可以使用 `--volume-from` 挂载数据卷：

```shell
$ docker run -it -v /dbdata --name dbdata ubuntu
$ docker run -it --volume-from dbdata --name db1 ubuntu
```

> **数据覆盖问题：**
>
> - 挂载一个空的数据卷到容器的非空目录：容器中目录下的文件会被复制到数据卷中。
> - 挂载一个非空的数据卷到容器的非空目录：容器中目录会显示数据卷中的内容，原来容器中目录下的内容会被隐藏。



