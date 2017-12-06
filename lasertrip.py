from gpiozero import LightSensor, InputDevice, OutputDevice
import time


ldr = InputDevice(25, pull_up = True)
ldr2 = InputDevice(8, pull_up = True)

#sseg
a = OutputDevice(5)
b = OutputDevice(9)
c = OutputDevice(19)
d = OutputDevice(13)
e = OutputDevice(6)
f = OutputDevice(11)
g = OutputDevice(26)
d1 = OutputDevice(21)
d2 = OutputDevice(20)

#keypad
r1 = InputDevice(17, pull_up = True)
r2 = InputDevice(4, pull_up = True)
r3 = InputDevice(3, pull_up = True)
r4 = InputDevice(2, pull_up = True)
c1 = OutputDevice(24)
c2 = OutputDevice(23)
c3 = OutputDevice(18)

count = 0
threshold = .8
print('started')

counter = 0
blocking = 0

disp_num = 0


class StateMachine:
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []
        self.loop = True
        self.handler = None

    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name.upper()

    def setup(self):
        try:
            self.handler = self.handlers[self.startState]
        except StateMachine:
            raise Exception("must call .set_start() before .run()")
        if not self.endStates:
            raise Exception("at least one state must be an end_state")

    def run(self, cargo1, cargo2):
        #print(self.handler)
        self.loop = True
        while self.loop:
            (new_state) = self.handler(cargo1, cargo2)
            print(new_state, cargo1, cargo2)
            if new_state.upper() in self.endStates:
                print("reached ", new_state)
                self.handler = self.handlers[new_state.upper()]
            else:
                self.handler = self.handlers[new_state.upper()]
                #print(self.handler)
            self.loop = False



def start_state(laser1, laser2):
    #print(laser1, laser2)
    if laser1 and not laser2:
        new_state = 'laser1_buffer'
    elif laser2 and not laser1:
        new_state = 'laser2_buffer'
    elif not laser1 and not laser2:
        new_state = 'start'
    else:
        new_state = 'invalid'
    return new_state


def buffer_one_state(laser1, laser2):
    #print(laser1, laser2)
    if laser1 and not laser2:
        new_state = 'start'
    elif laser2 and not laser1:
        new_state = 'entered'
    elif not laser1 and not laser2:
        new_state = 'laser1_buffer'
    else:
        new_state = 'invalid'
    return new_state


def entered_state(laser1, laser2):
    #print(laser1, laser2)
    global counter
    global blocking
    blocking = 0
    counter += 1
    print('counter = ', counter)
    if laser1 and not laser2:
        new_state = 'laser1_buffer'
    elif laser2 and not laser1:
        new_state = 'laser2_buffer'
    elif not laser1 and not laser2:
        new_state = 'start'
    else:
        new_state = 'invalid'
    return new_state


def buffer_two_state(laser1, laser2):
    #print(laser1, laser2)
    if laser1 and not laser2:
        new_state = 'exited'
    elif laser2 and not laser1:
        new_state = 'start'
    elif not laser1 and not laser2:
        new_state = 'laser2_buffer'
    else:
        new_state = 'invalid'
    return new_state


def exited_state(laser1, laser2):
    #print(laser1, laser2)
    global counter
    global blocking
    blocking = 0
    if counter > 0:
        counter -= 1
    else:
        counter = 0
    print('counter = ', counter)
    if laser1 and not laser2:
        new_state = 'laser1_buffer'
    elif laser2 and not laser1:
        new_state = 'laser2_buffer'
    elif not laser1 and not laser2:
        new_state = 'start'
    else:
        new_state = 'invalid'
    return new_state


def invalid(laser1, laser2):
    #print(laser1, laser2)
    new_state = 'start'
    return new_state


def start():
  global blocking, disp_num, count, counter
  global a, b, c, d, e, f, g, d1, d2
  global r1, r2, r3, r4, c1, c2, c3
  global ldr, ldr2
  maxcapacity = 0

  segments = [a, b, c, d, e, f, g]
  digits = [d1, d2]

  num = {' ':[],
        '0':[a, b, c, d, e, f],
        '1':[b, c],
        '2':[a,b,d,e,g],
        '3':[a,b,c,d,g],
        '4':[b,c,f,g],
        '5':[a,c,d,f,g],
        '6':[a,c,d,e,f,g],
        '7':[a,b,c],
        '8':[a,b,c,d,e,f,g],
        '9':[a,b,c,d,f,g],
         '10':[g]}

  ROW = [r1, r2, r3, r4]
  COL = [c1, c2, c3]
  MATRIX = [ [1, 2, 3],
           [4, 5, 6],
           [7, 8, 9],
           ['*', 0, '#'] ]
  for j in COL:
    j.on()
  
  n = 0
  numarray = []
  laser_a = False
  laser_b = False
  fq = 0
  ctr = 750

  try:
    while True:
      if int(maxcapacity) <= counter:
        disp_num = -1
      else:
        disp_num = counter
      if disp_num != -1:
        s = str(disp_num).rjust(2)
      else:
        s = '10'
      for dig in range(2):
        digits[dig].off()
        if disp_num != -1:
          digitSeg = num[s[dig]]
        else:
          digitSeg = num[s]
        for seg in digitSeg:
          seg.on()
        digits[dig].on()
        for seg in digitSeg:
          seg.off()
      for j in range(3):
        COL[j].off()
        for i in range(4):
          if ROW[i].value == True:
            while ROW[i].value == True:
              pass
            if(MATRIX[i][j] == '#' and n == 0):
              del numarray[:]
              print("Enter Number")
              n = 1
            elif(MATRIX[i][j] == '#' and n == 1):
              print("Number finished")
              n = 0
              print(''.join(str(e)for e in numarray))
              maxcapacity = ''.join(str(e)for e in numarray)
              disp_num = ''.join(str(e)for e in numarray)
            elif(MATRIX[i][j] != '#' and MATRIX[i][j] != '*' and n == 1):
              print(MATRIX[i][j])
              numarray.append(MATRIX[i][j])
            else:
              print("nothing to do")
        COL[j].on()
      fq = fq + 1
      if fq% ctr == 0:
        laser_a = ldr.value
        #print(laser_a, laser_b)
        laser_b = ldr2.value
        #print('laser2 ', laser_b)
        m.run(laser_a, laser_b)
      if laser_a or laser_b:
        blocking = blocking + 1
      if blocking > 100000000:
        print('stop blocking')
        blocking = 0
  except KeyboardInterrupt:
    print('sseg done')


if __name__ == "__main__":
    m = StateMachine()
    m.add_state('start', start_state)
    m.add_state('laser1_buffer', buffer_one_state)
    m.add_state('laser2_buffer', buffer_two_state)
    m.add_state('exited', exited_state, end_state=1)
    m.add_state('entered', entered_state, end_state=1)
    m.add_state('invalid', invalid, end_state=1)
    m.set_start('start')
    m.setup()
    start()

