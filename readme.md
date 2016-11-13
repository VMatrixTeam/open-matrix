# Open Matrix

> create by yejq Nov 13, 2016

## Introduction
Open Matrix 系统是Matrix系统的开源版本，提供一套完整的编程课程学习系统，包括：

- 课程学习
- 作业提交，自动评测
- QA系统
- 博客系统
....

## 系统架构
### 后台
- Python Tornado (web server)
- Pyjade (template engine)
- torndb (db access helper)

### 前端
- Bootflat (component based on bootstrap)

## 运行

### 基本依赖
- ubuntu 16.04
- python 2.7
- pip
- python development tools
- python mysql

### 运行命令
```shell

sudo apt-get install setuptools

cd /path/to/project/

sudo pip install -r requirements.txt

python server.py development

```

部分运行可能会报错，请检查依赖关系
