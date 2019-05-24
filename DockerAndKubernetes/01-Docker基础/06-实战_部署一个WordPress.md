# 实战：部署一个 WordPress

利用前面学过的 Docker 基础知识，部署一个 WordPress。

**步骤：**

- 获取 MySQL 和 WordPress 镜像
- 启动 MySQL 容器，注意配置 `MYSQL_ROOT_PASSWORD`
- 启动 WordPress 容器，使用 `--link` 与 MySQL 容器相连，注意将容器内的 80 端口映射到本地的 8080 端口上

**命令：**

```shell
# 获取 MySQL 和 WordPress 镜像
docker pull wordpress
docker pull mysql

# 启动 MySQL 容器


# 启动 WordPress 容器

```

