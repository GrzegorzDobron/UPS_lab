from time import sleep

output = []                 #bufor_wwrite()
for i in range(256):
    output.append("")
outpos = 0

mess = []                   #bufor_rread()
for i in range(256):
    mess.append("")
mess_pos = 0

buf = "1abcdefghijklmnoprstuwyz0"
#buf = "1aaa/0"

limits = 16                 #limit_znakow
pos=127

def rread():
    global pos
    pos=(pos+1)&127;
    #print("pos=", pos)
    if (pos >= (limits+1)):
        signal_success()
        return exit()
    else:
        return buf[pos];

def wwrite(data, num):      #wwrite(data,num):data-Tablica, num-Ilosc znakow
    global output
    global outpos
    for i in range(num):
        output[outpos]=data[i];
        outpos=(outpos+1)&256;

def delay():
    sleep(0.05)
def signal_success():
    print("success")
def signal_error():
    print("error")
def checkpoint():
    print("chechpoint")

class WaitState:
    def run(self):
        delay()
        c = rread();
        if(c=='1'):
            return ChannelStateMachine.readDataState
        else:
            return ChannelStateMachine.waitState

class ReadDataState:
    def run(self):
        global mess_pos
        global mess
        delay()
        c=rread();
        print(c)
        if(c == '\\'):
            return ChannelStateMachine.readBSlashState
        elif(c == '0'):
            wwrite(mess,mess_pos)
            mess_pos = 0
            signal_success()
            return ChannelStateMachine.waitState
        elif(c == '1'):
            mess_pos=0
            return ChannelStateMachine.readDataState
        else:
            mess[mess_pos] = c
            mess_pos = mess_pos + 1
            return ChannelStateMachine.readDataState

class ReadBSlashState:
    def run(self):
        global mess_pos
        global mess
        delay()
        c = rread();
        mess[mess_pos] = c;
        mess_pos = mess_pos + 1
        return ChannelStateMachine.readDataState

class ChannelStateMachine:
    waitState = WaitState()
    readDataState = ReadDataState()
    readBSlashState = ReadBSlashState()
    
    def __init__(self):
        self.currentState = ChannelStateMachine.waitState
        while (1):
            self.currentState = self.currentState.run()