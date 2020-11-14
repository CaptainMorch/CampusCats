# 快速部署教程
此教程将介绍最基础的部署与设置流程。若您已满足部署条件且具有一定网络开发基础，整个部署过程可能不超过5分钟。

## 简介
> Docker 是一个用于开发、装载和运行应用的容器。通过使应用与底层分离，docker 让应用能被快速分发。
>
> ——[Docker overview](https://docs.docker.com/get-started/overview/)

由于项目的各个部件都被 docker 容器化，整个项目都已经脱离底层运行在 docker 层上，所以只要能安装 docker 就可以实现几乎一键化的部署运行。

## 目录
0. [需求](#需求)
1. [安装 Docker](#安装-docker)
    1. [docker engine](#安装-docker-engine)
    2. [docker compose](#安装-docker-compose)
2. [下载并设置项目](#下载并设置项目)
3. [部署](#部署)
4. [Troubleshoot](#troubleshoot)

## 需求
- 任一 Linux 发行版的服务器，配置不限（位于国内则需备案）
- 没了

## 安装 docker
### 安装 docker engine
[docker 官方文档中的安装教程](https://docs.docker.com/engine/install/#server)

[gitee 中文安装教程](https://docker_practice.gitee.io/zh-cn/install/)

太长不看系列:
```bash
# 安装
curl -fsSL get.docker.com -o get-docker.sh
sudo sh get-docker.sh --mirror Aliyun

# 启动
sudo systemctl enable docker
sudo systemctl start docker

# 设置当前用户权限 (optional)
sudo groupadd docker
sudo usermod -aG docker $USER

# 测试 (optional)
docker run hello-world
```

## 安装 docker compose
[docker 官方文档中的安装教程](https://docs.docker.com/compose/install/)

[gitee 中文安装教程](https://docker_practice.gitee.io/zh-cn/compose/install.html)

太长不看系列:
```bash
# 安装
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 测试 (optional)
docker-compose --version
```

## 下载并设置项目
cd 进临时存放项目代码的目录，下载项目代码。可以手动下载代码压缩包再解压；

也可以直接把库克隆下来：
```bash
git clone https://github.com/CaptainMorch/CampusCats.git
```

OK， 现在设置项目：

- 编辑 [`./site_settings.py`](../site_settings.py) 如下：
  ```python
  # (可选)添加你的网站域名（不需要本地访问则删去前三项默认值）
  ALLOWED_HOST = ['localhost', '0.0.0.0', '127.0.0.1', 'yourhost.com']
  
  # 你的网站名称
  SITE_NAME = '某校的猫猫'
  ```
- 进入 [`./secrets`](../secrets) 填写所有文件：
  ```bash
  cd ./secrets
  echo 一个密码 > mysql_password.txt         # 设置数据库普通用户密码
  echo 一个密码 > mysql_root_password.txt    # 设置数据库 root 用户密码
  echo 一个密钥 > site_secret_key.txt        # 设置站点密钥（随机字符串）
  cd ../
  ```
- (可选) 如果了解且认为需要，再自行编辑 [`campuscats/campuscats/settings.py`](../campuscats/campuscats/settings.py)

## 部署
打包运行容器：
```bash
docker-compose up --build -d
```

打包完成后，还需等待后台执行半分钟左右的初始化，完成后即可正常访问。

确定网站可以正常访问后，执行以下命令新建后台管理员账号：
```bash
docker exec -it django python manage.py createsuperuser
```

至此网站部署完成。关于网站管理维护请点[此处](manage.md)

## Troubleshoot
- **"Got permission denied while trying to connect to the Docker daemon socket..."**

  要么把你自己和 docker 拉进一个用户组，要么每次用 `docker` 或者 `docker-compose` 都带上 `sudo`
  
- **部署时 docker 拉取镜像（mysql, nginx, python）过慢**
  
  [加速加速](https://docker_practice.gitee.io/zh-cn/install/mirror.html)
  
- **部署时 pip 下载包过慢**
  
  打开 [`campuscats/Dockerfile`](../campuscats/Dockerfile)，看到这几行代码，然后按照注释操作：
  ```dockerfile
  # 若网络环境位于国内，pip 默认源难以使用，
  # 则注释掉以下第一行，再启用第二行即可
  RUN pip install -r requirements.txt
  # RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```

- **打开任何页面均显示 400**
  
  检查 `ALLOWED_HOST =[]` 是否设置正确。从任何不在该列表中的 host 访问均会被默认拒绝
