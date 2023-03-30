# README

~目前服务已经部署在网络服务器~( 服务器到期，无法使用）

医学知识图谱及智能问答系统研究：后端部分

采用Flask框架，fuseki为数据库

本地配置方式：

* 修改data/dataCrawler代码，下载数据源
* 修改utils/rdfmaker代码，生成illness-info.rdf文件
* 启动apache-fuseki-server服务，新建medical_kbqa数据库，并添加illness-info.rdf文件到数据库中
* 运行medical_main.py，确保能正常运行

前端代码暂不提供。
