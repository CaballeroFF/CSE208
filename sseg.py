import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

segment = {'a': 29, 'b': 21, 'c': 35, 'd': 33, 'e': 31, 'f': 23, 'g': 37}
for seg in segment.itervalues(): 
  GPIO.setup(seg, GPIO.OUT)
  GPIO.output(seg, 0)
digit = [40, 38]
for dig in digit:
  print(dig) 
  GPIO.setup(dig, GPIO.OUT)
  GPIO.output(dig, 1)

num = {' ':[],
      '0':['a','b','c','d','e','f'],
      '1':['b','c'],
      '2':['a','b','d','e','g'],
      '3':['a','b','c','d','g'],
      '4':['b','c','f','g'],
      '5':['a','c','d','f','g'],
      '6':['a','c','d','e','f','g'],
      '7':['a','b','c'],
      '8':['a','b','c','d','e','f','g'],
      '9':['a','b','c','d','f','g']}

n = 12 

try:
  while True:
    s = str(n).rjust(2)
    for dig in range(2):
      GPIO.output(digit[dig], 0) 
      digitSeg = num[s[dig]]
      for seg in digitSeg:
        GPIO.output(segment[seg], 1)    
      GPIO.output(digit[dig], 1)    
      for seg in digitSeg:
        GPIO.output(segment[seg], 0)

except KeyboardInterrupt:
  GPIO.cleanup
