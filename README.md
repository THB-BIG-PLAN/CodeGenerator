## 项目介绍
本项目是一个基于Excel表格生成嵌入式软件应用层代码的工具。通过解析 config.xlsx 文件中的内容，自动整理出软件需求，并生成相应的应用层代码。同时，该工具具有检查软件需求冲突的功能，确保生成代码的正确性与合理性。

### 核心模块
该项目主要包含以下三个模块：

1. EVT（事件处理模块）
当满足 Condition 模块中的条件时， EVT 模块会通过函数指针跳转至对应的事件处理函数并执行相应操作。

2. Logic（逻辑调度模块）
负责整体逻辑调度，包括信号的同步与条件的判断。确保不同模块之间的协作与通信顺畅。

3. Condition（条件判断模块）
为了节省硬件的Flash空间， Condition 模块将多个判断条件转换为代码，并存储根据软件需求整理出的判断条件。

### 使用方式
1. 根据提供的config.xlsx文件填写软件需求
2. 通过cmd运行main.exe（注意cmd需要切换至exe所在路径，并且main.exe和config.xlsx必须在同一目录下）
3. 等待生成代码完成，生成的源码文件会分别保存在EVT、Logic、Condition三个文件夹中
4. 根据config.xlsx分析出信号可能的取值，并做笛卡尔积
5. 生成检查代码的脚本requirement_verifier.py，并自动执行，其中的信号输入来自于笛卡尔积，后一个场景的前态来自于前一个数据，并将结果输出到result.xlsx中

也可以直接运行main.py