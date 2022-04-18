from webbot import Browser 
from tabulate import tabulate
import pyttsx3
import threading
import datetime

# log in website regis
def browser():
    web = Browser()
    web.go_to('https://stdregis.ku.ac.th/_Login.php') 
    
    ### private data ###
    web.type('', number = 1) # StudentID
    web.press(web.Key.TAB + 'Boat2543!') # Password
    ### private data ###
    
    web.press(web.Key.ENTER)
    web.click('รายงาน')
    web.click('ผลการเรียน' , tag='a')
    raw_html = web.find_elements(id="Layer1")[0].get_attribute('outerHTML')
    web.quit()
    return raw_html

def getCourse(raw_html):
    Course = []
    pattern_start = '<td align="center" class="tr">'
    pattern_end = '</td>'
    index = 0
    length = len(raw_html)
    while index < length:
        start = raw_html.find(pattern_start, index)
        if start > 0:
            start = start + len(pattern_start)
            end = raw_html.find(pattern_end, start)
            link = raw_html[start:end]
            Course.append(link)
            index = end
        else:
            break
    return Course

def getCourseName(raw_html):
    Name = []
    pattern_start = '<font color="#000000">'
    pattern_end = '</font>'
    index = 0
    length = len(raw_html)
    while index < length:
        start = raw_html.find(pattern_start, index)
        if start > 0:
            start = start + len(pattern_start)
            end = raw_html.find(pattern_end, start)
            link = raw_html[start:end]
            Name.append(link)
            index = end
        else:
            break
    return Name

# create data
def create_data(course,course_name):
    data = []
    sub_data = []
    j = 1
    for i in range (1,len(course)+1):
        sub_data.append(course[i-1])
        if i % 3 == 1:
            sub_data.append(course_name[j-1])
            j+=1
        if i % 3 == 0:
            data.append(sub_data)
            sub_data = []
    # print(data)

    #define header names
    col_names = ["Course Code", "Course Title", "Grade", "Credit"]

    #display table
    # print(tabulate(data, headers=col_names))
    return data



########### only Second Semester 2021 (last term) ################
# print(len(data))
def check_update(data):
    engine = pyttsx3.init();

    data_term = []
    for i in range(61,65):
        data_term.append(data[i])

    #define header names
    col_names = ["Course Code", "Course Title", "Grade", "Credit"]

    #display table
    # print(tabulate(data_term, headers=col_names))

    res = tabulate(data_term, headers=col_names)
    prev_f = open("grade.txt", "r")
    prev_res = prev_f.read()
    prev_f.close()

    timeStamp = datetime.datetime.now()

    if prev_res != res:
        f = open("grade.txt", "w")
        f.write(res)
        f.close()
        msg = "Grade Announce at " + str(timeStamp)
        print(msg)
        engine.say(msg)
        engine.runAndWait()
        #display table
        print(tabulate(data_term, headers=col_names))
    else:
        msg = "no update at " + str(timeStamp)
        print(msg)
        engine.say(msg)
        engine.runAndWait()
    return ''

def main():
    threading.Timer(60.0, main).start()
    raw_html = browser()
    course = getCourse(raw_html)
    course_name = getCourseName(raw_html)
    data = create_data(course,course_name)
    check_update(data)

main()