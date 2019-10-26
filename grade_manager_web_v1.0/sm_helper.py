# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 20:51:34 2019

@author: 구상수
"""
import operator
from random import *
import pymysql

class StudentManager:
    def __init__(self):
        #f =  pen("C:/Users/구상수/.spyder-py3/study/grade.txt", 'r')
        #f = open("./grade.txt", 'r')

        #lines = f.readlines()
        #self._st_lines = lines
        self._conn = pymysql.connect(host='localhost', user='root', password='pham0615', db='stdb', charset='utf8')

    @staticmethod
    def get_ranking(st_ID, grade_dic):
        sorted_dic = sorted(grade_dic.items(), key=operator.itemgetter(1),reverse=True)
        #print(type(sorted_dic))
        #print(sorted_dic)
        #dic_keys= dict(sorted_dic).keys()
        count = 0
        #for i, dic_key in enumerate(dic_keys):
        for i, dic_key in enumerate(sorted_dic):
            dic_key = dic_key[0]
            #print ('dic_key:'dic_key)
            if st_ID == dic_key:
                count = i
                break
        # print ('initial:',count)
        while not(count==0):
            # print ('make : ',count)
            if count != 0 :
                if  sorted_dic[count][1]==sorted_dic[count-1][1]:
                    count -= 1
                else:
                    break    
        return count + 1

    """
    @staticmethod
    def get_ranking(st_name, grade_dic):
        sorted_dic = sorted(grade_dic.items(), key=operator.itemgetter(1),reverse=True)
        #dic_keys= dict(sorted_dic).keys()
        count = 0
        #for i, dic_key in enumerate(dic_keys):
        for i, dic_key in enumerate(sorted_dic):
            dic_key = dic_key[0]
            if st_name == dic_key:
                count = i + 1
                break
        while True:
            
        return count
    """


    def view_grade_old(self, name):
        for line in self.lines:
            if line.find(name) >= 0:
                print(line.split(':')[1])
                
                
    def student_clsranking(self, st_ID, st_name):
        
        st_class = int(str(st_ID)[1:3]) # something is strange
        curs = self._conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT ID, name, math+english+korean+physics+alchemy AS \"grade_sum\" \
               from STUDENT WHERE st_class={};".format(st_class)
        curs.execute(sql)
        rows = curs.fetchall()

        class_grades = {}
        for row in rows:
            '''line_split = line.split('_')
            temp_student = line_split[1].split(':')
            temp_grade = temp_student[1].split('\t')
            if line_split[0] == str(st_class):
                class_grades[temp_student[0]] = sum([int(g) for g in temp_grade])'''

            class_grades[row['ID']] = row['grade_sum'] 
        return [ self.get_ranking(st_ID, class_grades), len(class_grades) ]
                 
                     
    def view_student_grade(self, student_ID, name):
        """ View student grade
        Args : name(student name) 
        Returns : 0(null)
        """
        st_g = int(str(student_ID)[0:1])
        # student_cls = student_ID[1:3]
        curs = self._conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM STUDENT WHERE ID > {} and ID < {}".format(st_g*10000, (st_g+1)*10000)
        curs.execute(sql)
        rows = curs.fetchall()
        print (rows)

        avg = {}
        math = {}
        english = {}
        korean = {}
        physics = {}
        alchemy = {}
        '''
        lines = self._st_lines
        total = len(lines)
        print(lines[:5]) 
        '''       
        total = len(rows)
        # select DB
        for row in rows:
            st_class = row['st_class']
            #print(st_class)
            st_ID = row['ID']
            st_name = row['name']
            '''all_grade = line.split(':')[1].split('\t')
            sum = 0
            for x in all_grade:
                sum = sum + int(x)'''
            math[st_ID] = row['math']
            english[st_ID] = row['english']
            korean[st_ID] = row['korean']
            physics[st_ID] = row['physics']
            alchemy[st_ID] = row['alchemy']
            print('st_id L ', type(st_ID))
            print('input: ', type(student_ID))
            if st_ID == student_ID:
                print ('same')
            avg[st_ID] =(row['math']+row['english']+row['korean']+row['physics']+row['alchemy'])/5

        cls_ranking , cls_total = self.student_clsranking(st_ID, name)
        # calculating grade
        grade_report = {}
        grade_report['personal'] = [student_ID, name]
        grade_report['cls_ranking'] = [total,
                                        cls_ranking,
                                        cls_total,
                                        round(cls_ranking / cls_total * 100, 2)
                                        ]
        grade_report['avg'] = [avg[student_ID], 
                             StudentManager.get_ranking(student_ID, avg),
                             total,
                             round(StudentManager.get_ranking(student_ID, avg) / total * 100, 2)]
        grade_report['math'] = [math[student_ID], 
                             StudentManager.get_ranking(student_ID, math),
                             total,
#여기부터
                             round(StudentManager.get_ranking(student_ID, math) / total * 100, 2)]
        grade_report['english'] = [english[student_ID], 
                             StudentManager.get_ranking(student_ID, english),
                             total,
                             round(StudentManager.get_ranking(student_ID, english) / total * 100, 2)]
        grade_report['korean'] = [korean[student_ID], 
                             StudentManager.get_ranking(student_ID, korean),
                             total,
                             round(StudentManager.get_ranking(student_ID, korean) / total * 100, 2)]
        grade_report['physics'] = [physics[student_ID], 
                             StudentManager.get_ranking(student_ID, physics),
                             total,
                             round(StudentManager.get_ranking(student_ID, physics) / total * 100, 2)]
        grade_report['alchemy'] = [alchemy[student_ID], 
                             StudentManager.get_ranking(student_ID, alchemy),
                             total,
                             round(StudentManager.get_ranking(student_ID, alchemy) / total * 100, 2)]
        
        return grade_report


    def view_class_grade(self):

        curs = self._conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM STUDENT"
        curs.execute(sql)
        rows = curs.fetchall()
        class_grades = {}
        class_total = {}

        for row in rows:
            gclass = int(str(row['ID'])[0:3])
            if gclass not in class_grades.keys():
                class_grades[gclass] = row['math']+row['english']+row['korean']+row['physics']+row['alchemy']
                class_total[gclass] = 1
            else:
                class_grades[gclass] += row['math']+row['english']+row['korean']+row['physics']+row['alchemy']
                class_total[gclass] += 1
        
        class_avg = {}
        for cls_number in class_grades.keys():
            class_avg[cls_number] = round( class_grades[cls_number] / class_total[cls_number] , 2 )
        sorted_list = sorted(class_avg.items(), key=operator.itemgetter(1),reverse=True)
        sorted_dic = {}
        for i in sorted_list:
            sorted_dic[i[0]]=i[1]
        return sorted_dic

                
    
    def write_grade(self, ID, name, math, english, korean, physics, alchemy):
        curs = self._conn.cursor(pymysql.cursors.DictCursor)
        sql = """INSERT INTO STUDENT(ID, name, math , english, korean, physics, alchemy, st_class)
         values (%s, %s,%s, %s, %s, %s, %s, %s)"""
        st_class = int(str(ID)[1:3])
        curs.execute(sql, (ID, name, math, english, korean, physics, alchemy, st_class))
        self._conn.commit()
        return "Success"
#    @staticmethod
#    def write_rd_grade(loop):
#        
      

if __name__ == '__main__':
    
    sm = StudentManager()
    #sm.view_class_grade()
    #sm.write_grade(13, '구승재', 100, 50, 0, 10, 80)
    sm.view_student_grade(13,'구승재')
