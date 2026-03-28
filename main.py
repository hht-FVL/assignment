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