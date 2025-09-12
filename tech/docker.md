## ubuntu 安装：

> curl -sSL https://get.daocloud.io/docker | sh

## 重新构建

docker-compose --profile server up -d --build

## 核心概念

-   容器（Container）：轻量化的运行实例，包含应用代码、运行时环境和依赖库。基于镜像创建，与其他容器隔离，共享主机操作系统内核（比虚拟机更高效）。
-   镜像（Image）：只读模板，定义了容器的运行环境（如操作系统、软件配置等）。通过分层存储（Layer）优化空间和构建速度。
-   Dockerfile：文本文件，描述如何自动构建镜像（例如指定基础镜像、安装软件、复制文件等）。
-   仓库（Registry）：存储和分发镜像的平台，如 Docker Hub（官方公共仓库）或私有仓库（如 Harbor）。

## Docker Daemon

### 功能：

Docker 的核心服务进程
管理镜像、容器、网络和存储卷
监听 Docker API 请求并处理

### 主要职责：

镜像管理（构建、存储、分发）
容器生命周期管理
网络管理
数据卷管理
与 Registry 通信
