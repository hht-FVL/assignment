import os
import random
import time

class Student:
    def __init__(self, serial_num, name, gender, class_num, student_id, college):
        self.serial_num = serial_num  
        self.name = name              
        self.gender = gender          
        self.class_num = class_num   
        self.student_id = student_id  
        self.college = college       
    def __str__(self):
        return f"学生信息：\n学号：{self.student_id}\n姓名：{self.name}\n性别：{self.gender}\n班级：{self.class_num}班\n学院：{self.college}学院"
  
class ExamSystem:
    def __init__(self, file_path):
        self.file_path = file_path 
        self.student_list = []       
        self.total_student = 0       
        self._load_student_data()

    def _load_student_data(self):
        # 异常处理：文件不存在、读取失败等异常
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[1:]:
                    parts = line.strip().split('\t')
                    if len(parts) == 6:
                        serial_num = parts[0]
                        name = parts[1]
                        gender = parts[2]
                        class_num = parts[3]
                        student_id = parts[4]
                        college = parts[5]
                        student = Student(serial_num, name, gender, class_num, student_id, college)
                        self.student_list.append(student)
            self.total_student = len(self.student_list)
            print(f"学生数据加载成功！共加载{self.total_student}名学生信息")
        
        # 处理文件不存在的异常，给出友好提示
        except FileNotFoundError:
            print(f"错误：未找到学生名单文件，请检查路径{self.file_path}是否正确")
        # 处理其他未知异常
        except Exception as e:
            print(f"文件读取失败，发生未知错误：{str(e)}")
    @staticmethod
    def check_student_id_format(student_id):
        # 判断输入的学号是否为数字
       return student_id.strip().isdigit()

    # 按学号查找学生信息的核心方法
    def search_student_by_id(self, input_id):
        if not self.check_student_id_format(input_id):
            print("输入错误：学号必须为纯数字，请重新输入")
            return
  
        target_id = input_id.strip()
        # 遍历所有学生对象，匹配学号
        for student in self.student_list:
            if student.student_id == target_id:
                print(student)
                return
        # 遍历完成未匹配到，给出提示
        print(f"未找到学号为{target_id}的学生信息，请核对学号后重试")        

    def random_roll_call(self, input_count):
        # 异常处理：输入非数字的转换异常
        try:
            roll_count = int(input_count.strip())
        except ValueError:
            print("输入错误：点名数量必须为有效整数，请重新输入")
            return

        if roll_count < 1:
            print("输入错误：点名数量不能小于1")
            return
        if roll_count > self.total_student:
            print(f"输入错误：点名数量不能超过总人数{self.total_student}")
            return
        
        # 从学生列表中随机抽取不重复的指定数量学生
        roll_students = random.sample(self.student_list, roll_count)
        print(f"\n===== 随机点名结果（共{roll_count}人）=====")
        for index, student in enumerate(roll_students, start=1):
            print(f"{index}. 学号：{student.student_id}  姓名：{student.name}")
        print("==========================================\n")
        # 生成考场安排表核心方法
    def generate_exam_seat_plan(self):
        shuffled_students = self.student_list.copy()
        random.shuffle(shuffled_students)
        generate_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 定义输出文件路径，根目录下的「考场安排表.txt」
        output_file = "考场安排表.txt"

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"生成时间：{generate_time}\n")
                f.write("考场座位号\t姓名\t学号\n")
                # 遍历打乱后的学生，写入座位信息，座位号从1开始
                for seat_num, student in enumerate(shuffled_students, start=1):
                    f.write(f"{seat_num}\t{student.name}\t{student.student_id}\n")
            print(f"考场安排表生成成功！文件路径：{os.path.abspath(output_file)}")
            self.seat_plan = shuffled_students
        
        # 处理文件被占用、无权限的异常
        except PermissionError:
            print("错误：没有文件写入权限，请关闭已打开的「考场安排表.txt」后重试")
        except Exception as e:
            print(f"考场安排表生成失败：{str(e)}")   

    def generate_exam_tickets(self):
        if not hasattr(self, 'seat_plan') or len(self.seat_plan) == 0:
            print("未找到考场安排信息，正在自动生成考场安排表...")
            self.generate_exam_seat_plan()
        
        ticket_dir = "准考证"
        # 异常处理：捕获文件夹创建失败的异常
        try:
            # 创建文件夹，exist_ok=True表示文件夹已存在时不报错
            os.makedirs(ticket_dir, exist_ok=True)
            print(f"准考证文件夹创建成功，路径：{os.path.abspath(ticket_dir)}")
        except Exception as e:
            print(f"准考证文件夹创建失败：{str(e)}")
            return
        
        # 遍历考场安排，逐个生成准考证文件
        for seat_num, student in enumerate(self.seat_plan, start=1):
            # 生成文件名，座位号不足两位自动补0
            file_name = f"{seat_num:02d}.txt"
            # 拼接文件完整路径
            file_path = os.path.join(ticket_dir, file_name)

            # 异常处理：捕获单个文件写入异常，避免单个失败导致整体中断
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"考场座位号：{seat_num}\n")
                    f.write(f"姓名：{student.name}\n")
                    f.write(f"学号：{student.student_id}\n")
            except Exception as e:
                print(f"座位号{seat_num}的准考证生成失败：{str(e)}")
                continue
        print(f"所有准考证生成完成！共生成{len(self.seat_plan)}个准考证文件") 

if __name__ == "__main__":
    STUDENT_FILE = "人工智能编程语言学生名单.txt"
    exam_system = ExamSystem(STUDENT_FILE)
    if exam_system.total_student == 0:
        print("学生数据加载失败，程序退出")
        exit()

    # 控制台交互菜单，循环执行直到用户选择退出
    while True:
        # 打印功能菜单
        print("\n===== 学生信息与考场管理系统 =====")
        print("1. 按学号查询学生信息")
        print("2. 随机点名")
        print("3. 生成考场安排表")
        print("4. 批量生成准考证文件")
        print("0. 退出系统")
        print("===================================")
        # 获取用户输入的功能编号
        choice = input("请输入您要执行的功能编号：").strip()

        # 根据用户选择执行对应功能
        if choice == "1":
            input_id = input("请输入要查询的学生学号：")
            exam_system.search_student_by_id(input_id)
        elif choice == "2":
            input_count = input("请输入要点名的学生数量：")
            exam_system.random_roll_call(input_count)
        elif choice == "3":
            exam_system.generate_exam_seat_plan()
        elif choice == "4":
            exam_system.generate_exam_tickets()
        elif choice == "0":
            print("感谢使用，程序退出")
            break
        else:
            print("输入错误，请输入0-4之间的有效功能编号")
