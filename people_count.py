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
        print(self.handler)
        self.loop = True
        while self.loop:
            (new_state) = self.handler(cargo1, cargo2)
            if new_state.upper() in self.endStates:
                print("reached ", new_state)
                self.handler = self.handlers[new_state.upper()]
            else:
                self.handler = self.handlers[new_state.upper()]
                print(self.handler)
            self.loop = False


counter = 0


def start_state(laser1, laser2):
    print(laser1, laser2)
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
    print(laser1, laser2)
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
    print(laser1, laser2)
    global counter
    counter += 1
    print(counter)
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
    print(laser1, laser2)
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
    print(laser1, laser2)
    global counter
    if counter > 0:
        counter -= 1
    else:
        counter = 0
    print(counter)
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
    print(laser1, laser2)
    new_state = 'start'
    return new_state


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
    loop = True
    while loop:
        x = int(input('laser1'))
        y = int(input('laser2'))
        try:
            value = int(x)
            value = int(y)
        except ValueError:
            loop = False
            m.loop = False
        m.run(x, y)
