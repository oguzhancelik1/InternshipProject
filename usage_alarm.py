import subprocess
import logging 
from logging import handlers
import time
import json
import threading

from functools import partial


import os 
# Return information about disk space as a list (unit included)                     
# Index 0: total disk space                                                         
# Index 1: used disk space                                                          
# Index 2: remaining disk space                                                     
# Index 3: percentage of disk used                                                  
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])

# Return CPU temperature as a character string                                      
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

# Return RAM information (unit=kb) in a list                                        
# Index 0: total RAM                                                                
# Index 1: used RAM                                                                 
# Index 2: free RAM                                                                 
def getRAMinfo():
    pipe = subprocess.Popen('free',shell = True, stdout = subprocess.PIPE)
    ram_info_stdout = pipe.communicate()




    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])


# Return % of CPU used by user as a character string                                
def getCPUuse():
   
    pipe = subprocess.Popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'",shell=True,stdout = subprocess.PIPE)
    cpu_usage_stdout = pipe.communicate()[0]
    cpu_usage = cpu_usage_stdout.decode('iso-8859-1').strip()
    cpu_usage = cpu_usage.replace(',','.')
    cpu_usage=float(cpu_usage)
    return cpu_usage
#****************************************************** day13 functions **************** 
def get_program_load(program_name):
    pipe = subprocess.Popen("ps aux | "+"grep "+program_name, shell = True,stdout = subprocess.PIPE)
    # result = subprocess.check_output("ps aux | "+"grep "+program_name)
    #program_load_stdout= pipe.communicate()
    #print(type(program_load_stdout))
    
    # print(program_load_stdout[0])
    pids_dictionary={}
    for each in pipe.stdout:
        processes_array = []
        temp_array=[]
        x=1

        each = each.decode('utf-8')
        each_list = each.split()
        
        for i in each_list:
            
            if x<=10:
                processes_array.append(i)
                x=x+1
            else:
                temp_array.append(i)
         
        
        key_name = processes_array[1]
        del processes_array[1]

        temp_string = ''.join(temp_array)
        
        processes_array.append(temp_string)
        pids_dictionary.update({key_name : processes_array})
      
        
        # print(processes_array)
        # print(temp_array)
    return pids_dictionary

def prepare_logger(logger):
    handler_format = logging.Formatter('%(name)s-%(asctime)s-%(process)d-%(levelname)s-%(message)s')

    handler = logging.StreamHandler()
    handler.setLevel(logging.ERROR)
    handler.setFormatter(handler_format)

    logger.addHandler(handler)

    handler_2 = logging.FileHandler('file.log')
    handler_2.setLevel(logging.WARNING)
    handler_2.setFormatter(handler_format)
    
    logger.addHandler(handler_2)
    return logger

def read_json(filename):
    with open(filename, 'r') as f:
        filey_dict = json.load(f)
    return filey_dict


def read_json_single_process_usage(filey_dict):
   
    return filey_dict["singleProcessUsage"]
def read_json_smtp_info(filey_dict):

    #print(filey_dict["smtpInfo"])
    return filey_dict["smtpInfo"]

def read_json_ram_usage(filey_dict):
    return filey_dict['ramUsage']


def read_json_cpu_usage(filey_dict):
    return filey_dict['cpuUsage']


#no longer in use
def check_program_load(single_process_array,logger):
    starttime=time.time()
    counter = 1
    while counter<5:
        for i in range(len(single_process_array)):
            my_dict = single_process_array[i]
            program_name = my_dict['name']
            program_cpu_limit = float(my_dict['cpuLimitation'])
            program_ram_limit = float(my_dict['ramLimitation'])
            program_load_dictionary = get_program_load(program_name)
            for each in program_load_dictionary:
                print(each+' is a '+program_name+' process !')
    
                program_info_array = program_load_dictionary[each] 
                program_cpu_usage = float(program_info_array[1])
                program_ram_usage = float(program_info_array[2])
                
                if(program_cpu_usage > program_cpu_limit)or(program_ram_usage > program_ram_limit):
                    log_message=''
                    if((program_cpu_usage > program_cpu_limit)):
                        log_message = f'Warning! {program_name} process with the id of :  {each} ,is using too much CPU. It uses : %{str(program_cpu_usage)}'
                    
                        # this where the loggging happens for cpu usage
                        #logger.warning('Warning! '+program_name+' process with the id of :  '+ each+' ,is using too much CPU. It uses : %'+str(program_cpu_usage) )
                        #print(log_message)
                    if(program_ram_usage > program_ram_limit):

                        log_message =f'{log_message}  Warning! {program_name} process with the id of :  {each} ,is using too much RAM. It uses : %{str(program_ram_usage)}'
                        # this where the loggging happens for ram usage
                        #logger.warning('Warning! '+program_name+' process with the id of :  '+ each+' ,is using too much RAM. It uses : %'+str(program_ram_usage) )
                    
                    print(log_message)

                else:
                    print(program_name+' process with the id of : '+ each+' ,is a calm process : '+str(program_cpu_usage))
        time.sleep(5.0 - ((time.time() - starttime) % 5.0))        
        counter = counter + 1

#DAY14
def check_single_process_st(logger,my_dict):
    program_name = my_dict['name']
    program_cpu_limit = float(my_dict['cpuLimitation'])
    program_ram_limit = float(my_dict['ramLimitation'])
    program_load_dictionary = get_program_load(program_name)
    # print(program_load_dictionary)
    for each in program_load_dictionary:
        print(each+' is a '+program_name+' process !')

        program_info_array = program_load_dictionary[each] 
        program_cpu_usage = float(program_info_array[1])
        program_ram_usage = float(program_info_array[2])
        
        if(program_cpu_usage > program_cpu_limit)or(program_ram_usage > program_ram_limit):
            log_message=''
            if((program_cpu_usage > program_cpu_limit)):
                log_message = f'Warning! {program_name} process with the id of :  {each} ,is using too much CPU. It uses : %{str(program_cpu_usage)}'
            
                # this where the loggging happens for cpu usage
                #logger.warning('Warning! '+program_name+' process with the id of :  '+ each+' ,is using too much CPU. It uses : %'+str(program_cpu_usage) )
                #print(log_message)
            if(program_ram_usage > program_ram_limit):

                log_message =f'{log_message}  Warning! {program_name} process with the id of :  {each} ,is using too much RAM. It uses : %{str(program_ram_usage)}'
                # this where the loggging happens for ram usage
                #logger.warning('Warning! '+program_name+' process with the id of :  '+ each+' ,is using too much RAM. It uses : %'+str(program_ram_usage) )
            
            print(log_message)
            
        else:
            print(program_name+' process with the id of : '+ each+' ,is a calm process : '+str(program_cpu_usage))
#DAY15
def check_single_process(logger,sleep,repetition_numb,my_dict):
    if sleep==False:
        program_name = my_dict['name']
        program_cpu_limit = float(my_dict['cpuLimitation'])
        program_ram_limit = float(my_dict['ramLimitation'])
        program_load_dictionary = get_program_load(program_name)
        # print(program_load_dictionary)
        for each in program_load_dictionary:
            print(each+' is a '+program_name+' process !')

            program_info_array = program_load_dictionary[each] 
            program_cpu_usage = float(program_info_array[1])
            program_ram_usage = float(program_info_array[2])
            
            if(program_cpu_usage > program_cpu_limit)or(program_ram_usage > program_ram_limit):
                log_message=''
                if((program_cpu_usage > program_cpu_limit)):
                    log_message = f'Warning! {program_name} process with the id of :  {each} ,is using too much CPU. It uses : %{str(program_cpu_usage)}'
                
                    # this where the loggging happens for cpu usage
                    #logger.warning('Warning! '+program_name+' process with the id of :  '+ each+' ,is using too much CPU. It uses : %'+str(program_cpu_usage) )
                    #print(log_message)
                if(program_ram_usage > program_ram_limit):

                    log_message =f'{log_message}  Warning! {program_name} process with the id of :  {each} ,is using too much RAM. It uses : %{str(program_ram_usage)}'
                    # this where the loggging happens for ram usage
                    #logger.warning('Warning! '+program_name+' process with the id of :  '+ each+' ,is using too much RAM. It uses : %'+str(program_ram_usage) )
                
                print(log_message)
                
            else:
                print(program_name+' process with the id of : '+ each+' ,is a calm process : '+str(program_cpu_usage))
    else:
        i=0
        while i<repetition_numb:
            program_name = my_dict['name']
            program_cpu_limit = float(my_dict['cpuLimitation'])
            program_ram_limit = float(my_dict['ramLimitation'])
            program_load_dictionary = get_program_load(program_name)
            # print(program_load_dictionary)
            for each in program_load_dictionary:
                print(each+' is a '+program_name+' process !')

                program_info_array = program_load_dictionary[each] 
                program_cpu_usage = float(program_info_array[1])
                program_ram_usage = float(program_info_array[2])
                
                if(program_cpu_usage > program_cpu_limit)or(program_ram_usage > program_ram_limit):
                    log_message=''
                    if((program_cpu_usage > program_cpu_limit)):
                        log_message = f'Warning! {program_name} process with the id of :  {each} ,is using too much CPU. It uses : %{str(program_cpu_usage)}'
                    
                        # this where the loggging happens for cpu usage
                        #logger.warning('Warning! '+program_name+' process with the id of :  '+ each+' ,is using too much CPU. It uses : %'+str(program_cpu_usage) )
                        #print(log_message)
                    if(program_ram_usage > program_ram_limit):

                        log_message =f'{log_message}  Warning! {program_name} process with the id of :  {each} ,is using too much RAM. It uses : %{str(program_ram_usage)}'
                        # this where the loggging happens for ram usage
                        #logger.warning('Warning! '+program_name+' process with the id of :  '+ each+' ,is using too much RAM. It uses : %'+str(program_ram_usage) )
                    
                    print(log_message)
                    
                else:
                    print(program_name+' process with the id of : '+ each+' ,is a calm process : '+str(program_cpu_usage))
            
            time.sleep(5)
            i=i+1
            print('*****************************************************************************')    
                








#DAY15

def check_cpu(limitation,logger):
    i = 0
    check_results = []
    while i<4:
        cpu_usage = float(getCPUuse())
        check_results.append(cpu_usage)

        time.sleep(4)
        i=i+1
    if  all(check_results[index] > limitation for index in range(len(check_results))):
        print('your machine is fried')

    else:
        print([each for each in check_results])
        print('Nothing to worry love ;D')




#DAY14
# def check_cpu(limitation,logger):
#     cpu_usage = getCPUuse()
#     if(float(cpu_usage) > limitation):
#         #logger.warning('Hey your machine is on fire')
#         print('Hey your machine is on fire')

#     else:
#         print('Your machine seems to be doing fine')


def check_ram(limitation,logger):
    cpu_usage = getRAMinfo()
    if(float(cpu_usage) > limitation):
        #logger.warning('Hey your machine is on fire')
        
        print('Hey your machine is on fire')

    else:
        print('Your machine seems to be doing fine')

#DAY14
# def check_with_timer(method):
#     # starttime=time.time()
#     counter = 1
#     while counter < 5:
#         method()
#         print(counter)
#         time.sleep(5)
#         # time.sleep(5.0 - ((time.time() - starttime) % 5.0))
#         counter = counter + 1

def check_with_timer(logger,method,args):
    # starttime=time.time()
    counter = 1
    while counter < 5:
        method()
        print(counter)
        time.sleep(5)
        # time.sleep(5.0 - ((time.time() - starttime) % 5.0))
        counter = counter + 1
#no longer in use
# def check_cpu(limitation,logger):
#     starttime=time.time()

#     counter = 1
#     while counter<5:

#         cpu_usage = getCPUuse()
#         if(float(cpu_usage) > limitation):
#             #logger.warning('Hey your machine is on fire')
#             print('Hey your machine is on fire')

#         else:
#             print('Your machine seems to be doing fine')
#         time.sleep(5.0 - ((time.time() - starttime) % 5.0))
#         counter=counter+1

def main():
    logger = logging.getLogger(__name__)
    logger = prepare_logger(logger)

    filename = 'filey.json'
    dictized_json = read_json(filename)

    limitation_dict =read_json_cpu_usage(dictized_json)
    limitation = float(limitation_dict['limitation'])
    #check_cpu(limitation,logger)

    my_array = read_json_single_process_usage(dictized_json)
    # lambda allows passing in functions into a list without invoking them   
   
    
    
    single_process_list =[]
    for index in range(len(my_array)):

        single_process_list.append({'f': check_single_process, 'a': my_array[index]})
    #print(single_process_list)
    
    threads = []
    for function in range(len(single_process_list)):
        f = single_process_list[function]['f']
        arg = single_process_list[function]['a']
        func_passer = partial(f,logger,True,2)
        # func_passer(logger=logger,sleep=False,repetition_numb=2,my_dict=arg)
        # import sys
        # sys.exit(1)   
        t = threading.Thread(target= func_passer,args=(arg,))
        t.start()
        threads.append(t)

    t=threading.Thread(target=check_cpu,args=[limitation,logger])
    t.start()
    for each in threads:
        each.join()    
    t.join()






    import sys
    sys.exit(1)
    process_list = [{'f': check_single_process, 'a': [my_array[index], logger]} for index in range(len(my_array))]
    threads = []
    for process in range(len(process_list)):
        t = threading.Thread(target=check_with_timer, args=(lambda:process_list[process]['f'](*process_list[process]['a']),))
        t.start()
        threads.append(t)
        #t.join()

    for each in threads:
        each.join()
    
 

 
    

    #***********************    DAY14   *******************************its the same until process_list
    # t = threading.Thread(target=check_program_load,args= (my_array,logger,))
    # t.start()
    # t_other = threading.Thread(target=check_cpu,args= (limitation,logger,))
    # t_other.start()

    # threads = []    
    # for val in range(args.threadcount):
    #             t= threading.Thread(target=, args = ())
    #             t.start()
    #             threads.append(t)
                
    #         for val in threads:
    #             val.join()







    #*******************************    DAY13   *****************************
    
    import sys
    sys.exit(1)
    logger = logging.getLogger(__name__)
    logger = prepare_logger(logger)

    starttime=time.time()
    filename = 'filey.json'
    dictized_json = read_json(filename)

    # smtp_dictionary = read_json_smtp_info(dictized_json)

    # a= read_json_ram_usage(dictized_json)



    # my_array = read_json_single_process_usage(dictized_json)
    # check_program_load(my_array,logger)

    limitation_dict =read_json_cpu_usage(dictized_json)
    limitation = float(limitation_dict['limitation'])
    check_cpu(limitation,logger)
    
    
    



    # counter = 1
    # while counter<5:
    #     print ('lol')
    #     time.sleep(5.0 - ((time.time() - starttime) % 5.0))
    #     counter=counter+1
    

    




 
    
    #************************************** DAY12   ***************************************
    logger = logging.getLogger(__name__)
    handler_format = logging.Formatter('%(name)s-%(asctime)s-%(process)d-%(levelname)s-%(message)s')

    handler = logging.StreamHandler()
    handler.setLevel(logging.ERROR)
    handler.setFormatter(handler_format)

    logger.addHandler(handler)

    handler_2 = logging.FileHandler('file.log')
    handler_2.setLevel(logging.WARNING)
    handler_2.setFormatter(handler_format)

    logger.addHandler(handler_2)

    cre=('example@gmail.com', 'password')

    m_host=('smtp.gmail.com',587)
    

    log_to_mail_handler = logging.handlers.SMTPHandler(
        mailhost=m_host, 
        fromaddr="from@gmail.com",
        toaddrs= ["to@gmail.com"],
        subject= "The Logs",
        credentials=cre,
        secure=(),
        timeout= 10.0)
    
    log_to_mail_handler.setLevel(logging.WARNING)
    log_to_mail_handler.setFormatter(handler_format)
    logger.addHandler(log_to_mail_handler)

    with open('filey.json', 'r') as f:
        filey_dict = json.load(f)
    
    string_from_the_user = 'python'

    
    for each in filey_dict:
        if (each['name'] == string_from_the_user):
            program_name = each["name"]
            program_load_limitation = each["limitation"]

        # tell the user that the program does not exist 
        else:
            info = "No such program"     
            #print(info)
            
    
    program_load_dictionary = get_program_load(program_name)

    for each in program_load_dictionary:
        print(each)
    
    print(program_load_dictionary)
    
    
    for each in program_load_dictionary:
        program_info_array = program_load_dictionary[each] 
        program_cpu_usage = program_info_array[1]
        program_cpu_usage = float(program_cpu_usage)
        program_load_limitation = float(program_load_limitation)
        if(program_cpu_usage > program_load_limitation):
            # this where the loggging happens
            logger.warning('Warning! '+program_name+' process with the id of :  '+ each+' ,is an ambitious process : '+str(program_cpu_usage) )
            print(program_name+' process with the id of : '+ each+' ,is an ambitious process : '+str(program_cpu_usage))
        else:
            print(program_name+' process with the id of : '+ each+' ,is a calm process : '+str(program_cpu_usage))
            
    












    # #***************************************** DAY 11 ***************************
    # # data = subprocess.Popen(['ls', '-l', ], stdout = subprocess.PIPE)

    # # output = data.communicate()
    # # print(type(output))
    # # for each in output:
    # #     print(each)
   
    # handler = logging.StreamHandler()
    # handler.setLevel(logging.DEBUG)
    # handler_format = logging.Formatter('%(name)s-%(asctime)s-%(process)d-%(levelname)s-%(message)s')
    # handler.setFormatter(handler_format)

    # logger = logging.getLogger(__name__)
    # logger.addHandler(handler)

    # handler_2 = logging.FileHandler('file.log')
    # handler_2.setLevel(logging.ERROR)
    # handler_2.setFormatter(handler_format)
    # logger.addHandler(handler_2)

    # cre=('example@gmail.com', 'password')

    # m_host=('smtp.gmail.com',587)
    

    # log_to_mail_handler = logging.handlers.SMTPHandler(
    #     mailhost=m_host, 
    #     fromaddr="from@gmail.com",
    #     toaddrs= ["to@gmail.com"],
    #     subject= "The Logs",
    #     credentials=cre,
    #     secure=(),
    #     timeout= 10.0)
    
    # log_to_mail_handler.setLevel(logging.DEBUG)
    # log_to_mail_handler.setFormatter(handler_format)
    # logger.addHandler(log_to_mail_handler)

    # # CPU informatiom
    # #logging.basicConfig(format='%(asctime)s-%(process)d-%(levelname)s-%(message)s')
    # # logging.warning('This is a Warning')

    # cpu_usage = getCPUuse()
    # cpu_usage = (cpu_usage).split()[0]
    # cpu_usage = cpu_usage.replace(',','.')
    # # print(type(cpu_usage))
    # # print(repr(cpu_usage))
    # #cpu_usage = str(cpu_usage)
    # if (float(cpu_usage)<5):
    #     logger.warning('this is a warning')
    # else:
    #     logger.error('this is an error')    
    
    
    # with open('file.log', 'r') as file:
    #     keyword_string = file.read().replace('\n', ' ')
    #     keyword_string = keyword_string.split(' ')
    
    



    
        
            
   
    


        
    #CPU_temp = getCPUtemperature()
    
    # RAM information
    # Output is in kb, here I convert it in Mb for readability
    RAM_stats = getRAMinfo()
    RAM_total = round(int(RAM_stats[0]) / 1000,1)
    RAM_used = round(int(RAM_stats[1]) / 1000,1)
    RAM_free = round(int(RAM_stats[2]) / 1000,1)

    # Disk information
    DISK_stats = getDiskSpace()
    DISK_total = DISK_stats[0]
    DISK_free = DISK_stats[1]
    DISK_perc = DISK_stats[3]

    
    

if __name__ == '__main__':
    main()

