import time
def Manualmode(): #This is the function for starting the test and asking at what flow rates to perform the test
    Flow_List = [] #Array that will store flow rates to be tested
    Min_List = [] #array for time for each flow rate
    Sec_List= []
    while True:
        GPM = int(input('Enter the flow rate in GPM to be tested: ')) #User inputs GPM wanted for test
        if (GPM <= 16 and GPM>0):
            Flow_List.append(GPM) #Adds the input into the Test_String arrayTimemin= int(input('Enter the time to test this flowrate in minutes: '))
        else:
            print('That flowrate is not in range, please re-enter a flowrate in range')
            continue
        while True:
            Timemin= int(input('Enter the time to test this flowrate in minutes:'))
            Timesec= int(input('Enter the time to test this flowrate in seconds:'))
            if ((Timemin >= 1 and Timesec >=0) or (Timesec >= 30 and Timemin >= 0)):
                Min_List.append(Timemin)
                Sec_List.append(Timesec)
                break
            else:
                print('That time is too short, please re enter a time')
                continue
        Continue = int(input('Would you like to enter another test point?')) #The touchscreen will ask users to input more test points
        if Continue == 1: #If the user wants to add more values the test will not start yet
            print(Flow_List, Min_List, Sec_List)
            continue
        else: #if the user doesn't want to add values then the test will start
            break
    print(Flow_List, Min_List, Sec_List)
    Length = len(Flow_List)
    while Length > 0:
        pwm = HardwarePWM(pwm_channel=0, hz=2_000)
        pwm.start(5)
        time.sleep(20)
        Pump_flow = Flow_List[0]
        Test_min = Min_List[0]
        Test_sec = Sec_List[0]
        min2sec = Test_min*60
        Total_sec = min2sec + Test_sec
        print(Total_sec)
        Duty_cycle =(1-((((Pump_flow/16)*8)+2)/12))
        pwm.change_duty_cycle(Duty_cycle)
        time.sleep(20)
        for s in range(Total_sec, 0, -1):
            seconds = s % 60
            minutes = int(s / 60) % 60
            print("Time Remaining: "f"{minutes:02}:{seconds:02}")
            time.sleep(1) #Waits for 1 second before counting down again
        print("TIME'S UP!")
        #code for testing
        #code for testing
        #code for testing
        Flow_List.pop(0)
        Min_List.pop(0)
        Sec_List.pop(0)
        Length += -1
    return #returns array to be called in other function


Manualmode()


    
