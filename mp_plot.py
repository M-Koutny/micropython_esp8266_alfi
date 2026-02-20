from machine import Pin
from time import sleep_us
from alfi_font import *

class SM:
    def __init__(self, name, pins):
        self.name = name
        self.pins = pins
        self.pos = 0
        self.poff = 1
        self.ph = 0
        self.pin_objects = []
        
    def setup_pins(self):
        self.pin_objects = [Pin(pin, Pin.OUT) for pin in self.pins]
        self.sleep()

    def step(self, inc):
            self.ph += inc
            if self.ph<0 : self.ph=7
            if self.ph>7 : self.ph=0 
            self.pos += inc
            self.apply_phase()
            self.poff= 0

    def apply_phase(self):
        phases = [
            [1, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 1, 0, 1],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [1, 0, 1, 0],
            [1, 0, 0, 0] 
             ]
        
        for pin, state in zip(self.pin_objects, phases[self.ph]):
            if state==0:
				pin.on()
            else: pin.off()
	   
    def sleep(self):
        for pin in self.pin_objects:
            pin.on()
        self.poff= 1
            
    def set_pos(self,pos):
		self.pos=pos

    def get_status(self):
        return {
            'name': self.name,
            'pos': self.pos,
            'phase': self.ph,
            'poff':self.poff
        }

mdly=3800 # motor delay

#m_x = SM('X', [16, 17, 25, 26]) #wemos R1
m_x = SM('X', [0, 4, 5, 16]) #NodeMCU
m_x.setup_pins()

#m_y = SM('Y', [19, 23, 5, 13]) #wemos R1
m_y= SM('Y', [13,12,14, 2]) # NodeMCU
m_y.setup_pins()


def mv_mt(mt,inc=1,rng=1,dly=mdly):
	for i in range(rng):
		mt.step(inc)
		if rng>1: sleep_us(dly) #no dly for single step
	mt.sleep()	

#pn=Pin(18,Pin.OUT) #pen Wemos ESP32
pn=Pin(15,Pin.OUT) #pen NodeMCU
pn.on()  # on (~pen up inverted logic)

pd_dly=92000 #pen down delay
pu_dly=50000 #pen up delay


def penDown(dly=pd_dly):
    pn.off()
    sleep_us(dly)
    
def penUp(dly=pu_dly):
    pn.on()
    sleep_us(dly)

chrSc=2

def pltChr(chrCode,scl=chrSc):
    commands = { 0x1: [ 1,  0], 0x2: [ 0, -1], 0x3: [ 0,  1], 0x4: [ 1, -1], 0x5: [-1,  1], 0x6: [-1, -1], 
                0x7: [ 1,  1], 0x8: 'penDown', 0x9: 'penUp', 0xA: [ -1, 0], 0xB: 'end' }

    data = font[chrCode]
    #penUp()
            
    for byte in data:
        command = (byte & 0xF0) >> 4
        steps = byte & 0x0F
        m_x.sleep()
        m_y.sleep() 
        if (commands[command] == 'penUp'):
           penUp()
        elif (commands[command] == 'penDown'):
           penDown()
        elif (commands[command] == 'end'):
           #penUp()
           break
        else: 
             [dx,dy] = commands[command]
             for i in range(steps*scl):
               if (dx!=0): m_x.step(dx)
               if (dy!=0): m_y.step(dy)
               sleep_us(mdly)
     

def demo():
     m_x.set_pos(0)
     pltChr(154,8)
     for i in '   Toto je mala ukazka souradnicoveho zapisovace z Merkuru':
         pltChr(ord(i),3)
         mv_mt(m_x,1,3)

def next_line():
    mv_mt(m_y,1,70)
    mv_mt(m_x, -1, m_x.get_status()['pos'])
   
