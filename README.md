何泓韬-25362019-第二次人工智能编程作业

1.任务拆解与AI协作策略
步骤1：先让AI实现符合要求的Student数据类，确认__init__和__str__魔术方法
步骤2：让AI实现ExamSystem类的初始化方法
步骤3：实现学生信息按学号查找功能
步骤4：实现随机点名功能，重点要求AI处理ValueError异常
步骤5：实现考场安排表生成功能，符合生成时间、文件内容规范
步骤6：实现准考证批量生成功能
步骤7：让ai生成菜单，完成整个系统功能整合与测试

2.核心Prompt迭代记录
初代Prompt：
帮我用python写一个随机点名的功能，我输入数量，返回这个数量学生名单
AI生成的问题：
1.没有封装到ExamSystem类中，没有全局的思维
2.没有处理ValueError异常，输入字母会直接导致程序崩溃
优化后的Prompt：
请用python把随机点名功能封装为ExamSystem类的一个方法，要求：
必须用try-except处理输入非数字的ValueError异常，给出友好提示；
必须校验输入数量，不能小于1，也不能超过学生总人数；
仅使用Python标准库

3. Debug 与异常处理记录
报错：
运行生成准考证功能时，出现FileNotFoundError，报错信息显示系统找不到指定的路径。
解决过程：
1. 我先看懂了Traceback报错信息，定位到报错出现在文件写入的步骤；
2. 排查发现，AI生成的初代代码没有先创建文件夹，直接往不存在的文件夹里写入文件，导致报错；
3. 我手动修改了代码，添加了os.makedirs创建文件夹；
4. 修改完成后，重新运行程序，功能正常，所有准考证文件都能正确生成。

4. 人工代码审查
@staticmethod
def check_student_id_format(student_id):
    #判断输入的学号是否为纯数字
    return student_id.strip().isdigit()

#按学号查找学生信息的方法，封装在ExamSystem类中
def search_student_by_id(self, input_id):
    if not self.check_student_id_format(input_id):
        print("输入错误：学号必须为纯数字，请重新输入")
        return
    
    #去除输入学号的首尾空格
    target_id = input_id.strip()
    #遍历所有学生对象，逐个匹配学号
    for student in self.student_list:
        #匹配学生，打印完整信息
        if student.student_id == target_id:
            #调用Student类的__str__魔术方法
            print(student)
            return
    #遍历后未匹配到，给出提示
    print(f"未找到学号为{target_id}的学生信息，请核对学号后重试")
