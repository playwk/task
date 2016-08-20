#Author ZhengZhong,Jiang
import pickle
from prettytable import PrettyTable as pt
from conf import settings
from core import initialize


class course:
    def __init__(self, ID, name, cost, principal, context):
        self.ID = ID
        self.course_name = name
        self.course_cost = cost
        self.course_principal = principal
        self.course_context = context

    def learn_s(self):
        data_student = pickle.load(open('%s/student.db' % settings.DB_DIR, 'rb'))
        data_course = pickle.load(open('%s/course.db' % settings.DB_DIR, 'rb'))
        filed = ['课程ID', '课程名', '课时费用', '主讲']
        print_out = pt(filed)
        print_out.align['课程ID'] = '1'
        print_out.padding_width = 1
        for i in data_student.keys():
            print_out.add_row([i, data_student[i][0], data_student[i][1], data_student[i][2]])
        print(print_out)
        while True:
            choose_input = input('请选择要学习的课程：').strip()
            if choose_input not in data_student:
                print("选择无效！")
            else:
                print(data_course[choose_input][3])
            break


class teacher_add:
    def __init__(self, ID, name, password, assets=0):
        self.ID = ID
        self.name = name
        self.password = password
        self.assets = 0

class teacher:
    def __init__(self,ID):
        self.ID = ID

    def learn_t(self):
        data = pickle.load(open('%s/user.db' % settings.DB_DIR, 'rb'))
        data[self.ID][3] = int(data[self.ID][3]) + 500
        print('资产：%s ' % data[self.ID][3])
        pickle.dump(data, open('%s/user.db' % settings.DB_DIR, 'wb'))

    def extra(self):
        data = pickle.load(open('%s/user.db' % settings.DB_DIR, 'rb'))
        data[self.ID][3] = int(data[self.ID][3]) - 300
        print('资产：%s ' % data[self.ID][3])
        pickle.dump(data, open('%s/user.db' % settings.DB_DIR, 'wb'))


class student(course):
    def __init__(self, user_ID):
        self.user_ID = user_ID


    def learn(self):
        course.learn_s(self)

    @staticmethod
    def choose(user_ID):
        data_student = pickle.load(open('%s/student.db' % settings.DB_DIR, 'rb'))
        data_course = pickle.load(open('%s/course.db' % settings.DB_DIR, 'rb'))
        filed = ['课程ID', '课程名', '课时费用', '主讲']
        print_out = pt(filed)
        print_out.align['课程ID'] = '1'
        print_out.padding_width = 1
        for i in data_course.keys():
            print_out.add_row([i, data_course[i][0], data_course[i][1], data_course[i][2]])
        print(print_out)
        choose = input('请选择：').strip()
        if choose not in data_course.keys():
            print("选择无效！")
        else:
            if choose not in data_student:
                data = pickle.load(open('%s/student.db' % settings.DB_DIR, 'rb'))
                data[user_ID] = [choose, data[choose][0], data[choose][1], data[choose][2]]
                pickle.dump(data, open('%s/student.db' % settings.DB_DIR, 'wb'))
                print('选课成功！')
            else:
                print("该课程已添加！")




def login():
    data = pickle.load(open('%s/user.db' % settings.DB_DIR, 'rb'))
    while True:
        userID_input = input("请输入用户ID：").strip()
        password_input = input("请输入密码：")
        if userID_input not in data:
            print('该用户不存在！')
        else:
            if password_input == data[userID_input][1]:
                if data[userID_input][2] == '0':
                    stu = student(userID_input)
                    while True:
                        print("""
    1.选课
    2.上课
    其他任意键退出！""")
                        choose_input = input('请选择： ')
                        if choose_input == '1':
                            stu.choose(userID_input)
                        elif choose_input == '2':
                            stu.learn_s()
                        else:
                            exit()
                elif data[userID_input][2] == '1':
                    tea = teacher(userID_input)
                    while True:
                        print("""
    1.缺课
    2.上课
    其他任意键退出！""")
                        choose_input = input('请选择： ')
                        if choose_input == '1':
                            tea.extra()
                        elif choose_input == '2':
                            tea.learn_t()
                        else:
                            exit()
                else:
                    print("""
    1.创建课程
    2.添加老师
    其他任意键退出""")
                    choose_input = input("请选择： ")
                    if choose_input == '1':
                        data_course = pickle.load(open('%s/course.db' % settings.DB_DIR, 'rb'))
                        while True:
                            course_ID = input('请输入课程ID：').strip()
                            if course_ID not in data_course:
                                course_name = input('请输入课程名：').strip()
                                course_cost = input('请输入课时费：')
                                course_principal = input('请输入主讲老师：')
                                course_context = input('请输入课程内容：')
                                course_obj = course(course_ID, course_name,
                                                    course_cost, course_principal, course_context)
                                data_course[course_ID] = [course_name,course_cost,course_principal, course_context]
                                pickle.dump(data_course, open('%s/course.db' % settings.DB_DIR, 'wb'))
                                print("添加成功！")
                                break
                            else:
                                print('课程ID重复')
                    elif choose_input == '2':
                        data_user = pickle.load(open('%s/user.db' % settings.DB_DIR, 'rb'))
                        while True:
                            teacher_ID = input('请输入老师ID：').strip()
                            if teacher_ID not in data_user:
                                teacher_name = input('请输入老师名：').strip()
                                teacher_pwd = input('请输入老师密码：')
                                teacher_obj = teacher_add(teacher_ID, teacher_name, teacher_pwd, '1')
                                data_user[teacher_ID] = [teacher_name, teacher_pwd, '1', teacher_obj.assets]
                                pickle.dump(data_user, open('%s/user.db' % settings.DB_DIR, 'wb'))
                                print('添加成功！')
                                break
                            else:
                                print('老师ID重复')
                    else:
                        exit()
            else:
                print('密码错误！')


def register():
    data = pickle.load(open('%s/user.db' % settings.DB_DIR, 'rb'))
    while True:
        userID_input = input('请输入注册ID: ').strip()
        if userID_input not in data:
            break
        else:
            print("该ID已被占用")
    username_input = input('请输入用户名：').strip()
    password_input = input('请输入密码：')
    print('输入注册类型，学生输入0，老师输入1，管理员输入2')
    while True:
        role_input = input('请输入角色：').strip()
        if role_input == '0' or role_input == '1' or role_input == '2':
            break
        else:
            print('无效用户类型')
    data[userID_input] = [username_input, password_input, role_input]
    pickle.dump(data, open('%s/user.db' % settings.DB_DIR, 'wb'))


def main():
    print("""
    1. 登录
    2. 注册
    """)
    choose = input('请选择：').strip()
    if choose == '1':
        login()
    elif choose == '2':
        register()
    else:
        print('无效输入，退出！')
        exit()