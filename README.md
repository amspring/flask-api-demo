# flask demo 

#### 介绍
基于Flask框架， 采用flask_restful提供API的WEB项目架构

#### 设计功能模块
> 初始化数据库脚本  
> 接口缓存减少数据库连接  
> JWT Token 验证  
> 消息任务队列

#### 软件架构
```text
app                 -- 代码
    endpoints       -- 
        __init__.py -- 蓝图注册
        routes.py   -- 路由
    repositories    -- DB, 与数据库交互
    services        -- 业务处理
    middleware      -- 中间件
        celery.py   -- 队列注册
        cor.py      -- 跨域注册
        csrf.py     -- 防跨站
        database.py -- 数据库注册
        exception.py -- 异常注册
        redis.py    -- 缓存注册
    __init__.py     -- 注册
    conf.py         -- 读取config.yml
    config.py       -- flask 配置项
    containers.py   -- 依赖注入
    exceptions.py   -- 异常
    initialize.py   -- 数据库初始化
    logger.py       -- 日志
    models.py       -- models
    redis.py        -- redis
    resp.py         -- 返回初始化
    schemas.py      -- 参数验证, 如果参数过多, 建议拆分, 继承公告参数
    auth.py         -- 加密解密, token
    utils.py        -- 公共方法
config              -- 配置
    api.ini         --supversior 配置
    job.ini         --supversior 配置
    config.example.yml  --配置文件模板
    nginx.conf      --nginx配置参考
logs                --日志
.gitignore          --git 忽略文件
boot.sh             --生产环境部署脚本
cmd.py              --启动文件
prod.py             --生产环境配置
config.py           --Flask 参数配置
config.yml          --配置文件
docker-compose.yml  --docker compose
Dockerfile          --dockerfile
README.md           --文档
requirements.txt    --依赖包
```

#### 安装依赖包, 建议 Python 3.10.x  以上版本
```shell
pip install -r requirements.txt
```

#### 复制配置, 填写对应的账户数据
```text
cp config/config.example.yml config.yml
```

### 数据库初始化
一. 
##### 
```text
新建数据表
flask data --action create

删库跑路
flask data --action drop

删库再重建
flask data --action reset
```

二. 
#### 更新表格字段
https://flask-migrate.readthedocs.io/en/latest/
```text
新建迁移文件
flask db init

生成迁移脚本
flask db migrate -m "Initial migration."

执行脚本
flask db upgrade
```
三. 
##### 初始化添加管理员
```shell
flask admin --username "老六" --mobile "13599998888" --email "123@dd.com"
```

#### 终端shell
```shell
flask shell
```

#### 查看路由
```shell
flask routes
```

#### 开发环境
```shell
python cmd.py

1. 定时任务 beat 进程启动方式
celery -A cmd.celery beat -l info

2. 定时任务 worker 进程启动方式
celery -A cmd.celery worker -l info -P eventlet
```

#### 生产环境
linux环境, windows缺少 fcntl 模块
```shell
gunicorn -c prod.py cmd:app

1. 定时任务 beat 进程启动方式
celery -A cmd.celery beat -l info

2. 定时任务 worker 进程启动方式
celery -A cmd.celery worker -l info -P eventlet
```
