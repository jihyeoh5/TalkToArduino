import paramiko
import serial
def submit_jobs_server(command,host_job_server,usr_job,pass_job):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host_job_server, username=usr_job, password=pass_job)
    status = ssh_client.get_transport().is_active()
    stdin, stdout, stderr = ssh_client.exec_command(command)
    Version = (stdout.readlines())
    ssh_client.close()
    return Version
command = 'sqjobs'
host_job_server = 'saw.sharcnet.ca'
usr_job = 'jh6oh'
pass_job = "ILoveCoding"
sqinfo = submit_jobs_server(command,host_job_server,usr_job,pass_job)

#Find button labels
jobs = []
uButtons = []
cButtons = []
for lines in sqinfo[2:]:
    #Make list of status & job titles
    lines = lines.split()
    if lines: 
        jobs.append([lines[2],lines[len(lines)-1][:lines[len(lines)-1].find('.')]])
    if "uracil" in jobs[len(jobs)-1][1]: buttons = uButtons
    if "cytosine" in jobs[len(jobs)-1][1]: buttons = cButtons
    #Find first number that appears after "_"
    try:
        index = jobs[len(jobs)-1][1].index("_")
        if jobs[len(jobs)-1][1][index+1:index+3].isdigit() == True: #if double digit
            buttons.append(jobs[len(jobs)-1][1][index+1:index+3])
        else: buttons.append(jobs[len(jobs)-1][1][index+1])
    #If "_" not in job title
    except ValueError: buttons.append("0")
    if buttons == uButtons and len(buttons)>3: maxuButton = int(max(buttons))
    if buttons == cButtons and len(buttons)>3: maxcButton = int(max(buttons))
try:
    uButtons = [maxuButton-2,maxuButton-1,maxuButton]
    if maxuButton==0 or maxuButtons==1: uButtons = [maxuButton]
    if maxuButtons==2: uButtons = [1,2]
except NameError: pass
try:
    cButtons = [maxcButton-2,maxcButton-1,maxcButton]
    if maxcButton == 0 or maxcButton == 1: cButtons = [maxcButton]
    if maxcButtons==2: cButtons = [1,2]
except NameError: pass

#Set up dictionary for D/Q/R values
dictAll = {}
dictAll = dictAll.fromkeys(["dictc","dictu"])
dictAll["dictu"] = {}
dictAll["dictu"] = dictAll["dictu"].fromkeys(uButtons)
dictAll['dictc'] = {}
dictAll['dictc'] = dictAll["dictc"].fromkeys(cButtons)
methodList = ["pm6", "hf", "opt", "freq", "mp2"]
for j in range(len(jobs)): #For all jobs
    for k in range(len(uButtons)): #1/2/3 
        if "uracil" not in jobs[j][1]: continue
        index = jobs[j][1].index("_")
        if jobs[j][1][index+1:index+1+len(str(uButtons[k]))]==str(uButtons[k]): #if #W=#W
            #Find method by searching for last "_"
            methodIndex = int(jobs[j][1][len(jobs[j][1]):index:-1].index("_"))*-1-1
            method = jobs[j][1][methodIndex+1:]
            if method not in methodList: method = "opt"
            #Place D/Q/R value into corresponding method key
            try: dictAll['dictu'][uButtons[k]][method].append(jobs[j][0])
            except KeyError:
                dictAll['dictu'][uButtons[k]][str(jobs[j][1][methodIndex+1:])] = [jobs[j][0]]
            except TypeError:
                dictAll['dictu'][uButtons[k]]= {}
                dictAll['dictu'][uButtons[k]].setdefault(method),[jobs[j][0]]
    for k in range(len(cButtons)):
        if "cytosine" not in jobs[j][1]: continue
        index = jobs[j][1].index("_")
        if jobs[j][1][index+1:index+1+len(str(cButtons[k]))]==str(cButtons[k]):
            methodIndex = int(jobs[j][1][len(jobs[j][1]):index:-1].index("_"))*-1-1
            method = jobs[j][1][methodIndex+1:]
            if method not in methodList: method = "opt"
            try: dictAll['dictc'][cButtons[k]][method].append(jobs[j][0])
            except KeyError:
                dictAll['dictc'][cButtons[k]][str(jobs[j][1][methodIndex+1:])] = [jobs[j][0]]
            except TypeError:
                dictAll['dictc'][cButtons[k]]= {}
                dictAll['dictc'][cButtons[k]].setdefault(method,[jobs[j][0]])
print(dictAll)

#Produce "string" to send to Arduino
def writeStatus(dictButton):
    methodStatus = []
    for i in range(len(methodList)):
        try: 
            if "R" not in dictButton[methodList[i]] and "Q" not in dictButton[methodList[i]]:
                methodStatus.append("D"+methodList[i])
            elif "R" in dictButton[methodList[i]]:
                methodStatus.append("R"+methodList[i])
            elif "Q" in dictButton[methodList[i]] and "R" not in dictButton[methodList[i]]:
                methodStatus.append("Q"+methodList[i])
        except TypeError: continue
        except KeyError: continue
    methodLine = ','.join(methodStatus)
    methodLine = methodLine + ";"
    return str.encode(methodLine)

#Read button pressed on Arduino
arduino = serial.Serial("COM3", 9600)
while True:
    data = arduino.readline()[:-1].decode()
    print(data)
    if "button1" in data:
        try:
            dictButton = dictAll["dictu"][uButtons[0]] #Allow button to access specific dictionary
            arduino.write(writeStatus(dictButton)) #Write to Arduino
        except IndexError: continue
    elif "button2" in data:
        try:
            dictButton = dictAll["dictu"][uButtons[1]]
            arduino.write(writeStatus(dictButton))
        except IndexError: continue
    elif "button3" in data:
        try:
            dictButton = dictAll["dictu"][uButtons[2]]
            arduino.write(writeStatus(dictButton))
        except IndexError: continue
    elif "button4" in data:
        try:
            dictButton = dictAll["dictc"][cButtons[0]]
            arduino.write(writeStatus(dictButton))
        except IndexError: continue
    elif "button5" in data:
        try:
            dictButton = dictAll["dictc"][cButtons[1]]
            arduino.write(writeStatus(dictButton))
        except IndexError: continue
    elif "button6" in data:
        try:
            dictButton = dictAll["dictc"][cButtons[2]]
            arduino.write(writeStatus(dictButton))
        except IndexError: continue




