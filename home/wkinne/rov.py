######################################################
# A script to control the ROV
######################################################

# create the arduino service
arduino = Runtime.createAndStart("arduino", "Arduino")
arduino.connect("COM4")
 
# create services for the 3 motors on the rov
rightMotor = Runtime.createAndStart("rightMotor", "Motor")
leftMotor = Runtime.createAndStart("leftMotor", "Motor")
rearMotor = Runtime.createAndStart("rearMotor", "Motor")
xservo = Runtime.createAndStart("xservo","Servo")
yservo = Runtime.createAndStart("yservo","Servo")
 
# create the joystick service
joystick = Runtime.createAndStart("joystick", "Joystick")
 
# set the pins on the motors 
rearMotor.setPwrDirPins( 3, 4)
rightMotor.setPwrDirPins( 7, 8)
leftMotor.setPwrDirPins( 5, 6)

xservo.attach(arduino,26)
yservo.attach(arduino,28)

xservo.map(-1,1,0,180)
yservo.map(-1,1,0,180)

# attach the motors to the arduino so they can be controlled
rightMotor.attach(arduino)
leftMotor.attach(arduino)
rearMotor.attach(arduino)
 
# subscribe to the publishJoystickInput (this will call "onJoystickInput" in python 
python.subscribe("joystick","publishJoystickInput") 

# choose which controller
joystick.setController(3) 

# initialize the values for x and y so they're not null
x = 0
y = 0

################################################################
# This is the joystick callback method
# each button push will call this method with the button id and the value of that button..
################################################################
def onJoystickInput(data): 
  # define the x and y variables as global
  global x
  global y
  update = False
  # a debug statement to print the data being returned from the joystick
  print(data, data.id, data.value)
  
  # ry & rx run the camera gimbal  
  
  if data.id == u'ry':
     print("button ry is ", data.value)
  if data.id == 'ry':
     yservo.moveTo(data.value)
  if data.id == 'rx':
     print("button rx is ", data.value)
  if data.id == u'rx':
     xservo.moveTo(data.value)
  if data.id == u'x':
     # assign the value to the global variable "x"
     x = data.value
     update = True
     print("button x is ", data.value)
  if data.id == u'y':
     # assign the joystick value to the global variable y
     y = data.value
     update = True
  
  # z runs the rear motor, pick up the rear of the ROV and move forward to dive
  #                        lower the rear of the ROV and move forward to surface
  
  if data.id == 'z':
     print("axis z is ", data.value)
  if data.id == 'z':
     rearMotor.move(data.value)
     
  # at this point we have the latest values for x and y saved in global memory
  # compute the values to send to the motors
  
  if update:
     lefty=y+x             
     righty=y-x
 
     # send the values to the motors.
  
     leftMotor.move(lefty)
     rightMotor.move(righty)
