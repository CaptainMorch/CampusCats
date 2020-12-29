# 管理教程

## 基本管理
```bash
docker-compose up    # 启动
docker-compose exec web [command]    # 执行某命令
docker-compose exec web python manage.py shell    # django shell
```

## 本地测试
比如自行修改了 models 文件需要 makemigrations 时，不希望运行 docker，则可以使用本地测试的模板设置文件 [`settings/__dev_settings.py`](../settings/__dev_settings.py) 进行配置。同时还需要将该文件设置入环境变量，以使 django 可以找到：
```bash
cp ./settings/__dev_settings.py ./campuscats/dev_settings.py
export DJANGO_SETTINGS_MODULE=dev_settings

cd ./campuscats
# eg. python3 manage.py makemigrations
```
