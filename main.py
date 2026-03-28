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