from pad4pi import rpi_gpio
import time
import RPi.GPIO as GPIO
from firebase import firebase
import socket

from time import sleep



GPIO.setwarnings(False)
# Setup Keypad
KEYPAD = [
        ["1","2","3","A"],
        ["4","5","6","B"],
        ["7","8","9","C"],
        ["*","0","#","D"]
]

# same as calling: factory.create_4_by_4_keypad, still we put here fyi:

ROW_PINS = [4,17,27,22] # BCM numbering
COL_PINS = [12,16,20,21] # BCM numbering


factory = rpi_gpio.KeypadFactory()
firebase = firebase.FirebaseApplication('https://final-project-e264b.firebaseio.com',None)

# Try factory.create_4_by_3_keypad
# and factory.create_4_by_4_keypad for reasonable defaults


keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
imei=[]

        


def connwifi ():

    TCP_IP = '192.172.2.250'
    TCP_PORT = 8000
    BUFFER_SIZE = 20  # Normally 1024, but we want fast response
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
   
    
   
    conn, addr = s.accept()
    
    print ('Connection address:', addr)
    
    
    #conn.close()
    s.close()
    
    
    return ('True')
    
    
    



def decrypt(v,s):
    result = ""
    for i in range(len(v)):
        char = v[i] 
  
        result += chr((ord(char) -s) % 128)
    return result





def printKey(key):
    print(key)
    
    imei.append(key)
    if(key=="#"):
        
        #lock()
        imei.remove("#")
        #imei=list(im)
        #print("hello")
        print(imei)
        
        strr=""
        for x in imei:
            strr+=x
        print(strr)
        sts=connwifi()
        if(sts=='True'):
           
            result =firebase.get('/user/IMEI_NUMBER',None)
            #print(result)
            #resultDel=firebase.delete('/user/IMEI_NUMBER',None)
            list=[]
            list=result.values()
           

            for p in list:
                t=p
                print(t)
            #print(t)
            #for k,v in t.iteritems():
             #   print(v)
            #print(v)

        s = 5
        x=decrypt(t,s)
        print(x)


        #print("database"+v)
        #print("keypad"+strr)
        if(x == strr):
            print("Matched!")
            lock()
           # print(v)
            #print(strr)
        else:
            print("not matched")
        
        exit()
  
  
# printKey will be called each time a keypad button is pressed

print("Register imei:")


keypad.registerKeyPressHandler(printKey)



def lock():
    relay_pin = 26
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay_pin, GPIO.OUT)
    GPIO.output(relay_pin, 1)
    GPIO.output(relay_pin, 0)
    sleep(2)
    GPIO.output(relay_pin, 1)
    sleep(2)
    
    #try:
       # while True:
     #       GPIO.output(relay_pin, 0)
      #      sleep(2)
       #     GPIO.output(relay_pin, 1)
        #    sleep(2)
            
    #except KeyboardInterrupt:
     #           pass
   
    GPIO.cleanup()
    #connwifi()



try:
    while(True):
        time.sleep(0.2)
except:
    keypad.cleanup()




