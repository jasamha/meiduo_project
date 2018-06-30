[TOC]
## 美多商城
### git命令
push到远程并在远程创建dev分支:git push origin dev:dev
### 项目结构
```
父目录是meiduo_mall
├── docs        # 项目相关资料保存目录
├── logs         # 项目运行时/开发时日志目录
├── manage.py
├── meiduo_mall    # 开发时的代码保存
│   ├── apps   # 开发者的代码保存目录，以模块[子应用]为目录保存
│   ├── libs      # 第三方类库的保存目录
│   ├── settings.py
│   ├── urls.py
│   ├── utils     # 多个模块[子应用]的公共函数类库
└── scripts    # 保存项目运营时的脚本文件
```
### 自动导包
* sys.path(list):设置python解释器自动导包的路径   
* 可以新增一个导包路径到这个列表中，那么就不需要写太长的路径了。     
* sys.path.insert(0,需要导入的路径)
### debug配置和release配置
在父目录meiduo_mall中新建settings包,然后定义dev.py和release.py文件,把默认生成的settings拖到settings内容赋值到dev.py下,并在manage.py下修改配置
### 在序列化器中要获取视图类中数据  格式：self.context['view'].kwargs['变量名']
### redis管道技术
Redis 管道技术可以在服务端未响应时,客户端可以继续向服务端发送请求，并最终一次性读取所有服务端的响应.  