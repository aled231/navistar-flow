import RPi.GPIO as g
import './excel-function' as excel
from time import as sleep
g.setMode(g.BCM)
g.setup(2, g.IN)
revcount  = 0

def increaserev(channel):
    global revcount
    revcount += 1

g.add_event_detect(2, g.RISING, callback=increaserev)
while True:
    sleep(60)
    print("RPM is {0}".format(revcount))
    revcount = 0


if (button_pressed == True):
    excel.send_excel_file(config.email_address)
