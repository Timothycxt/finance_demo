# 项目结构
- manager.py：项目管理文件，入口
- App
    - \_\_init__.py：初始化文件
    - config.py：全局项目配置
    - extensions.py：拓展库管理（与路由相关的除外）
    - apis：路由（接口url）
    - models：定制模型，封装一些方法
[![JjgwsU.md.png](https://s1.ax1x.com/2020/05/02/JjgwsU.md.png)](https://imgchr.com/i/JjgwsU)

# 本地调试
运行manager.py文件，`edit configuration`里的`parameter`加上`runserver`

# 部署
1\. 上传项目到服务器

2\. 在 Dockerfile 文件所在目录，构建名为finance的镜像： 
```bash
docker build -t finance .
```  
3\. 运行容器
```bash
docker run -d -p 9003:8888 finance --restart=always
```