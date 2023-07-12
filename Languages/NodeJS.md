在倚天上使用 Node.js

# 1. 安装 Node.js

## 1.1. 使用 docker 镜像

根据需要的 Node 版本选择，如应用无特殊依赖需求可以根据版本选择 alpine 镜像，如 `18-alpine`/`16-alpine`，以获得更轻量的镜像。
如对依赖和环境有特殊要求，Node 提供了基于 Debian 的镜像：`18-buster`、`18-buster-slim`等。

## 1.2. 使用 Noslate Anode 发行版

[Noslate Anode](https://github.com/noslate-project/node) 是一个开源的 Node.js 下游发行版，
针对 Serverless 场景和 ARM 环境进行了优化。

Noslate Anode 的更多信息和二进制版本可以在 https://github.com/noslate-project/node 获得。

## 1.3. 使用 nvm 等 Node 版本管理工具安装

使用 nvm 可在本地安装并管理多个 Node / npm 版本，极大方便了本地开发，不推荐用于生产环境部署。

安装 nvm：
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
```

安装 node
```bash
$nvm install 16
$nvm use 16
$npm --version
8.11.0
```

## 1.4. 通过源码编译Node解释器

手动编译 Node 需要重新编译 v8 引擎，所需时间较长且并无可见收益，不推荐。

## 1.5. 使用操作系统包管理器安装Node

操作系统包管理器中的 Node 版本往往较低，无法获得最新的功能支持。

## 1.6. 推荐版本

- 推荐使用新版本的 Node.js。随着 Node.js 以及 v8 的更新，用户可以从上游的功能及性能更新中受益。
- 推荐至少使用 Node v18。v18 为目前活跃的长期支持（LTS）版本。
