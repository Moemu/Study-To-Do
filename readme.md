# 前言

这是一个比赛作品，但是它并没有取得它该有的成绩。

现在该作品的作者Moemu将其在Github开源，打算在明年继续参加该比赛。

# 概述

Study to do(学习待办) 是一款致力于学习任务整理，学习情况分析的一款应用软件，对学习计划安排能力强的学生适用。其灵感来源于Microsoft to do(微软待办)，但 Study to do 在学习数据整理方面体现出的优势比 Micosoft to do 较强。旨在帮助用户管理学习任务，了解学科所用时间占比，以帮助用户调整学习计划。

# 组成

Study To Do 应指导员建议，分为2个版本

第一个版本: Study To Do 3.x (Student/Normal) 一般发行版本，拥有绝大多数功能。

第二个版本: Study To Do 2.x (Teacher) 教师特供版本，用于下发作业和检查作业完成情况

# 部署

1. Clone此仓库，并配置Python 3.x 环境

2. 配置第三方库: `pip install -r requirements.txt `

3. 运行`Setup.py`以复制程序所需文件

4. 若要使用在线功能，你需要配置Leancloud服务器，您可以参考[设置Leancloud数据库](https://waline.js.org/guide/get-started.html#leancloud-设置-数据库)中的配置方法，得到里面的AppID和AppKey，并更改`account.py`,`student.py`中的以下代码:

   ```python
   leancloud.init('APPID','APPKEY') #源代码实际为leancloud.init('','')
   ```

5. 在使用在线功能中您可能遇到类错误，此时请至Leancloud应用中找到结构化数据并创建以下Class:

   `Class_list`,`Class_Member`,`Homework_list`,`Homework_Status`,`Plan`

# 有关安装包获取

由于数据库安全问题，我们不提供该应用的安装包（内含数据库密钥），如要获得完整的使用体验，请发issue申请。

# 文档

您可以在这里查看Study To Do的参赛时写的使用帮助页面，请注意，该文档没有部署教程

[Study to do 帮助文档 (muspace.top)](https://doc.muspace.top/#/zh-cn/Program/Study-To-Do)

# 关于

Study To Do (学习代办) 

版权所有: Moemu

不得以任何方式传播此应用源码