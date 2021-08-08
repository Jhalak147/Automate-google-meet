import time
import calendar
import pyautogui as auto
import schedule
import webbrowser 
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


opt=Options()
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
#pass argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", { 
"profile.default_content_setting_values.media_stream_mic": 1,
"profile.default_content_setting_values.media_stream_camera": 1,
"profile.default_content_setting_values.geolocation": 0,
"profile.default_content_setting_values.notifications": 1
})
driver = webdriver.Chrome(options=opt)

# TIME TABLE HERE
subjects = {'monday' : ['UNIX', 'OOAD', 'CD', 'OS', 'DBMS'],
            'tuesday' : ['UNIX', 'OOAD', 'CD', 'OS', 'DBMS'],
            'wednesday' : ['CD', 'OOAD', 'C','DBMS', 'OS'],
            'thursday' : ['CD', 'OOAD', 'C','DBMS', 'OS'],
            'friday' : ['OOAD', 'PEHV', 'CD',  'OS', 'UNIX'],
              }

# GOOGLE MEET LINKS TO RESPECTIVE SUBJECTS
classes = { 'UNIX':	'https://meet.google.com/sig-aczw-qkd',
            'PEHV':'https://meet.google.com/gps-uasv-wdt',
            'CD':'https://meet.google.com/sig-aczw-qkd',
            'C':'https://meet.google.com/gps-uasv-wdt',
            'OOAD':'https://meet.google.com/gps-uasv-wdt',
            'OS':'https://meet.google.com/imo-fgwh-jod',
            'DBMS':'https://meet.google.com/gps-uasv-wdt',
}

# CHANGE ACCORDING TO YOUR CLASS TIMINGS
timings = [['10:05',' 11:00'],['11:00','12:00'], ['12:00','13:00'],['14:00','15:00'],['15:00','16:00']]

# RETURNS CURRENT DAY
def find_day():
    date_and_time = datetime.now()
    date = str(date_and_time.day) + ' ' + str(date_and_time.month) + ' ' + str(date_and_time.year)
    date = datetime.strptime(date, '%d %m %Y').weekday()
    day = calendar.day_name[date]
    return day.lower()

# RETURNS INDEX FROM TIMININGS LIST THAT MATCHES WITH CURRENT TIME
def class_time():
        time = datetime.now().strftime("%H:%M")
        for i in range(0,len(timings)):
            if(timings[i][0]<=time<=timings[i][1]):
                return i
        return -1

# RETURNS THE SUBJECT WHOSE CLASS HAS TO BE ATTENDED 
def subject():
    classtime=class_time()
    day = find_day()
    for k,v in subjects.items(): 
        if k == day:
           return (v[classtime])

# RETUENS THE URL OF THE CLASS AS PER SCHEDULE
def meeting_link():
    clas=subject()
    if clas in classes.keys():
        return classes[clas]

while(True):
    ite_no=class_time()
    print(ite_no)
    if(ite_no==-1):
        break
    else:
        url=meeting_link()
        # driver = webdriver.Chrome(executable_path="C:\seleniumWebdrivers\chromedriver")
        driver.get('https://accounts.google.com/ServiceLogin/signinchooser?ltmpl=meet&continue=https%3A%2F%2Fmeet.google.com%3Fhs%3D193&&o_ref=https%3A%2F%2Fwww.google.com%2F&_ga=2.233774365.2056812406.1627629038-1664641889.1626238180&flowName=GlifWebSignIn&flowEntry=ServiceLogin')

        
        #Logs in the classroom
        username=driver.find_element_by_id('identifierId')
        username.click()
        username.send_keys('Enter your email here') #Enter your email here

        next=driver.find_element_by_xpath('//*[@id="identifierNext"]')
        next.click()
        time.sleep(5)

        password=driver.find_element_by_xpath('//input[@type="password"]')
        password.send_keys('Enter your password here') #Enter your password here
        

        next=driver.find_element_by_xpath('//*[@id="passwordNext"]')
        next.click()
        time.sleep(15)
        
        driver.get(url)
        time.sleep(7)

        # turns off camera
        auto.hotkey('ctrl','e')
        # turns off mic
        auto.hotkey('ctrl','d')

        # clicks join button
        join=driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[4]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/span/span')
        join.click() 
        time.sleep(3)


        # END MEETING
        currenttime =datetime.now().strftime("%H:%M")
        
        t = str(datetime.strptime(timings[ite_no][1], '%H:%M')- datetime.now().strptime(currenttime,"%H:%M"))
        h, m, s = t.split(':')
        time.sleep(int(h) * 3600 + int(m) * 60 + int(s))
        end=driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[10]/div[2]/div/div[7]/span/button')
        end.click()



