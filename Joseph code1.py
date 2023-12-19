import tkinter as tk
from tkinter import  ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter  import PhotoImage
from tkinter import *
from PIL import ImageTk, Image
import time
import pigpio
import fly_email
import threading as th
from rpi_hardware_pwm import HardwarePWM

from datatest3 import generate_excel_file
       
class FlowRateAppClient:
    def startAutoFunc(self):
        self.thread = th.Thread(target=self.loop_measure)
        self.is_running=True
        self.thread.start()
        self.Automode()
        
    def startManualFunc(self):
        self.thread = th.Thread(target=self.loop_measure)
        self.is_running=True
        self.thread.start()
        self.Manualentry()
    
    def __init__(self, root):
        self.root = root
        self.root.title("Navistar Flow Meter Test Bench")
        self.root.configure(bg='lightblue')

        #Start and Stop buttons
        self.start_mal = ttk.Button(root, text="Start Manual", command=self.startManualFunc,style='Large.TButton')
        self.start_auto = ttk.Button(root, text="Start Automatic", command=self.startAutoFunc,style='Large.TButton')
        self.stop_button = ttk.Button(root, text="Stop Measurement", command=self.stop_measurement, state=tk.DISABLED,style='Large.TButton')

        self.start_mal.grid(row=0,column=0,padx=10,pady=10)
        self.start_auto.grid(row=1, column=0)
        self.stop_button.grid(row=1, column=1, padx=10, pady=10)
        
        #Create Menu
        menu = tk.Menu(root)
        root.config(menu=menu)
        
        filemenu = tk.Menu(menu)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='New',command=self.refresh_window)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=root.quit)
        
        self.tabs = ttk.Notebook(root,style="Custom .TNotebook")
        self.tabs.grid(row=0, column=1, padx=40, pady=40)

        # Additional buttons
        email_frame = ttk.Frame(self.tabs)
        email_frame.pack(fill='both',expand=True)
        #command=fly_email.latest_filepath
        self.tabs.add(email_frame, text="Email")
        self.entry= ttk.Entry(email_frame)

        #entry= ttk.Entry(email_frame,command='largofargo785@gmail.com')
        self.entry.grid(row=0,column=0,padx=20,pady=20)
        self.email_button = ttk.Button(email_frame, text="Send Email",command=self.send_email)
        self.email_button.grid(row=0,column=1,padx=20,pady=20)
        
        # Create a custom ttk style for larger buttons
        self.style = ttk.Style()
        self.style.configure('Large.TButton', font=('Helvetica', 20), padding=15)

        # Measurement variables
        self.is_measuring = False
        self.is_running = False
        self.flow_rate_value = 0
        self.waterflow = 0
        self.turbinegpm = 0
        self.time_intervals = []  # To store time intervals for the waveform plot
        self.flow_rate_history = []  # To store flow rate data for the waveform plot

    def reactivate_email_button(self):
        self.email_button.config(text="Send Email2", state=ACTIVE)

    def stop_measurement(self):
        self.is_measuring = False
        self.is_running = False
        self.start_auto.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)
    
    def Automode(self): #This is the function for starting the test and asking at what flow rates to perform the test
        self.start_mal.destroy()
        self.start_auto.destroy()
        is_measuring=True
        self.root.update()
        pwm = HardwarePWM(pwm_channel=0, hz=2_000)
        pwm.start(71)
        time.sleep(30)#waiting for valve, we can change this time based on testing
        #here we start code for reading data.
        pwm.change_duty_cycle(58)
        time.sleep(30)#waiting for valve, we can change this time based on testing
        #here we start code for reading data.
        pwm.change_duty_cycle(46)
        time.sleep(30)#waiting for valve, we can change this time based on testing
        #here we start code for reading data.
        pwm.change_duty_cycle(33)
        time.sleep(30)#waiting for valve, we can change this time based on testing
        #here we start code for reading data.
        pwm.change_duty_cycle(21)
        time.sleep(30)#waiting for valve, we can change this time based on testing
        #here we start code for reading data
        is_measuring=False
        pwm.stop()
    
    def measure_flow_rate(self):
        if self.is_measuring:
            flowGPIO = 17
            pi = pigpio.pi()
            pi.set_mode(flowGPIO, pigpio.INPUT)
            flowCallback = pi.callback(flowGPIO)
            pulse_count = 0
            while True:
                time.sleep(1)
                count = flowCallback.tally()
                self.waterflow = count - pulse_count
                pulse_count = count
                #pulses_meter1 = GPIO.input(self.flow_meter1_pin)
                #pulses_meter2 = GPIO.input(self.flow_meter2_pin)

                #flow_rate_meter1 = pulses_meter1 * 0.1  # Simulated calculation
                #flow_rate_meter2 = pulses_meter2 * 0.1  # Simulated calculation
            
                self.turbinegpm = self.waterflow/165
            
                self.flowlabel = Label(text="Flowrate ="f"{self.turbinegpm:01}")
                self.timelabel.grid(row=2, column=3)
                self.root.update()

                #self.flow_meter1_values.append(flow_rate_meter1)
                #self.flow_meter2_values.append(flow_rate_meter2)

                self.flow_rate_label.configure(text=f"Flow Rate Meter 1: {flow_rate_meter1:.2f} GPM")#, Flow Rate Meter 2: {flow_rate_meter2:.2f} GPM")

                #self.flow_rate_history.append(flow_rate_meter1)
                #self.time_intervals.append(len(self.flow_rate_history) * 2)  # 2-second intervals

            #timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
            #filename = f"flowMeterData_{timestamp}.txt"
            #self.write_to_file(filename, flow_rate_meter1)#, flow_rate_meter2)

            #self.root.after(2000, self.measure_flow_rate)
    
    def loop_measure(self):
        while(self.is_running):
            self.measure_flow_rate()

    def write_to_file(self, filename, gpm_meter1, gpm_meter2):
        with open(filename, "a") as file:
            if file.tell() == 0:  # File is empty, write headers
                file.write("Time Interval\tTurbine Sensor (GPM)\tElectromagnetic Sensor (GPM)\n")
            file.write(f"{len(self.time_intervals) * 2}\t{gpm_meter1:.2f}\t{gpm_meter2:.2f}\n")
    
    def send_email(self):
        filename = generate_excel_file()
        sender = 'horsepowerrpi@gmail.com'  # Update with your email address
        recipient = self.entry.get()  # Update with the recipient's email address
        subject = 'Flow Rate Data'
        body = 'Here is the flow rate data as requested.'
        #attachment_file = fly_email.get_iso_filenames('./', '.*\.xlsx')
        attachment_file = filename


        if attachment_file:
            success = fly_email.send_email(sender, recipient, subject, body, attachment_file)
            if success:
                print(f'Email sent successfully to {recipient} with attachment: {attachment_file}')
                self.entry.delete(0, 'end')

            else:
                print('Failed to send email.')
        else:
            print('No attachment file found to send in the email.')
        # Add your code to send an email with flow rate data
        pass

    def refresh_window(self):
        # Destroy existing widgets and recreate the GUI
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)

    def Manualentry(self): #This is the function for starting the test and asking at what flow rates to perform the test
        Length1 = len(self.Flow_List)
        if Length1 >0:
            self.yes.destroy()
            self.no.destroy()
            self.Question.destroy()
        self.start_mal.destroy()
        self.start_auto.destroy()
        self.GPMf= ttk.Entry(width=5)
        self.GPMf.grid(row=0,column=0,padx=10,pady=10)
        self.cont=ttk.Button(text = 'Enter Flowrate', command=self.cont_manual, style='Large.TButton')
        self.cont.grid(row=1, column=0, padx=10, pady=10)
    
    Flow_List = [] #Array that will store flow rates to be tested
    Min_List = []
    Sec_List = []
    Flow_quest = []
    Time_quest = []

    def cont_manual(self):
        GPMf = self.GPMf.get()
        GPM = int(GPMf)
        self.GPMf.delete(0, 'end')
        if (GPM <= 16 and GPM>0):
            self.Flow_List.append(GPM) #Adds the input into the Test_String arrayTimemin= int(input('Enter the time to test this flowrate in minutes: '))
            self.Minute_entry()
        else:
            self.Flow_quest.append(GPM)
            self.GPMf.destroy()
            self.cont.destroy()
            self.flow_text = Label(text = 'That flowrate is not in range, please re-enter a flowrate in range')
            self.flow_text.grid(row=2,column=1)
            self.Manualentry()
    
    def Minute_entry(self): #This is the function for starting the test and asking at what flow rates to perform the test
        F_length = len(self.Flow_quest)
        if F_length > 0:
            self.flow_text.destroy()
        self.cont.destroy()
        self.GPMm = ttk.Entry(width=5)
        self.GPMm.grid(row=0,column=0,padx=10,pady=10)
        self.contmin = ttk.Button(text = 'Enter Minutes', command=self.cont_manual_time, style='Large.TButton')
        self.contmin.grid(row=1, column=0, padx=10, pady=10)

    def cont_manual_time(self):
        GPMm = self.GPMm.get()
        self.GPMm.delete(0, 'end')
        self.Timemin = int(GPMm)
        print(self.Timemin)
        self.Seconds_entry()

    def Seconds_entry(self): #This is the function for starting the test and asking at what flow rates to perform the test
        self.contmin.destroy()
        self.GPMsec = ttk.Entry(width=5)
        self.GPMsec.grid(row=0,column=0,padx=10,pady=10)
        self.contsec = ttk.Button(text = 'Enter Seconds', command=self.cont_sec_time, style='Large.TButton')
        self.contsec.grid(row=1, column=0, padx=10, pady=10)

    def cont_sec_time(self):
        GPMsec = self.GPMsec.get()
        self.GPMsec.delete(0, 'end')
        Timesec = int(GPMsec)
        if ((self.Timemin >= 1 and Timesec >=0) or (Timesec >= 30 and self.Timemin >= 0)):
            self.Min_List.append(self.Timemin)
            self.Sec_List.append(Timesec)
            self.ask_quest()
        else:
            self.GPMm.destroy()
            self.contmin.destroy()
            self.contsec.destroy()
            self.GPMsec.destroy()
            self.Time_quest.append(Timesec)
            self.time_text = Label(text = 'That total test time is not in range, please re-enter minutes followed by seconds')
            self.time_text.grid(row=2,column=1)
            self.Minute_entry()

    def ask_quest(self):
        T_length = len(self.Time_quest)
        if T_length > 0:
            self.time_text.destroy()
        self.contsec.destroy()
        self.GPMf.destroy()
        self.GPMm.destroy()
        self.GPMsec.destroy()
        self.root.update()
        self.Question = ttk.Label(width=19,wraplength=120,text='Would you like to enter another value? Or start the test now?')
        self.Question.grid(row=0, column=0)
        self.yes = ttk.Button(text = 'Enter another value', command=self.Manualentry, style='Large.TButton')
        self.yes.grid(row=1, column=0, padx=10, pady=10)
        self.no = ttk.Button(text = 'Start test now', command = self.ManualUI, style='Large.TButton')
        self.no.grid(row=2, column=0)
        
    def ManualUI(self):
        self.no.destroy()
        self.yes.destroy()
        self.Question.destroy()
        self.root.update()
        self.ManualTimer()

    def ManualTimer(self):
        is_measuring=True
        Length = len(self.Flow_List)
        print(self.Flow_List, 'gpms')
        print(self.Min_List, 'minutes')
        print(self.Sec_List, 'seconds')
        #pwm = HardwarePWM(pwm_channel=0, hz=2_000)
        #pwm.start(5)
        while Length > 0:
            Pump_flow = self.Flow_List[0]
            Test_min = self.Min_List[0]
            Test_sec = self.Sec_List[0]
            min2sec = Test_min*60
            Total_sec = min2sec + Test_sec
            print(Total_sec)
            Duty_cycle =100*(1-((((Pump_flow/16)*8)+2)/12))
            #pwm.change_duty_cycle(Duty_cycle)
            time.sleep(5)
            for s in range(Total_sec, 0, -1):   
                self.measure_flow_rate()
                seconds = s % 60
                minutes = int(s / 60) % 60
                self.timelabel=Label(text="Time Remaining: "f"{minutes:02}:{seconds:02}")
                self.timelabel.grid(row=2, column=1)
                self.root.update()
                time.sleep(1) #Waits for 1 second before counting down again
                
            print("TIME'S UP!")
            
            
            #code for testing
            #code for testing
            #code for testing
            self.Flow_List.pop(0)
            self.Min_List.pop(0)
            self.Sec_List.pop(0)
            Length += -1
        is_measuring=False
        return #returns array to be called in other function


    
        
#-------------------------------------------------------------------------------------------------------------------   

def main():
    root=tk.Tk()
    
    app= FlowRateAppClient(root)
    root.mainloop()

if __name__ == "__main__":
    main()
