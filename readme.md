## plotplot
interfacing with the eibot board; this stepper and servo controller is sold by EMSL, Sparkfun and others.  It is designed by Brian Schmalz of Schmalz Haus. 

Here's what we're up to: http://tristanperich.com/Art/Machine_Drawings/images/Perich_Tristan_Machine_Drawing_Philoctetes_Small_Process.jpg
 - see also: http://tristanperich.com/Art/Machine_Drawings/
 - and: http://www.flickr.com/photos/geekphysical/sets/72157625827981787/with/5407732000/


### EMSL steppers
documented here: http://evilmadscience.com/productsmenu/partsmenu/187-stepper
1.8deg/set (200 steps per rotation)
connections to the EIBot board: http://cdn2.evilmadscience.com/im/eggbot/desc/2_800.jpg (I had brown in place of white)


### Commands
Fully described here http://www.schmalzhaus.com/EBB/EBBCommands.html
 
 - The most important command seems to be SM; from the docs:

```
The "SM" Command (stepper motor move)
Format: "SM,<duration>,<axis1>,<axis2><CR>"
<duration> is a value from 1 to 65,535 and is in milliseconds. It represents the total length of time you want this move to take. 
<axis1> and <axis2> are values from -32,767 to +32,767 and represent the number of steps for each motor to take in <duration> milliseconds.  If both <axis1> and <axis2> are zero, then a delay of <duration> ms is executed. <axis2> is an optional value, and if it is not included in the command, zero steps are assumed for axis 2.
Use this command to make the motors draw a straight line at constant velocity. The maximum speed that the EBB can generate is 25,000 steps/s. It is helpful to use this command with zeros for both <axis> parameters after moving the pen up or down to give it time to finish moving before starting the next motor move.

Example: "SM,1000,250,-766"
Return Packet: "OK"
```

 - EM is also rather important for setting the step mode:

```
The "EM" Command (enable motors) for EBB v1.2 and above

Format: "EM,<Enable1>,<Enable2><CR>"
To enable a motor driver, set its <Enable> parameter to 1. 
To disable a motor driver, set its <Enable> parameter to 0.
For example, "EM,1,0" will enable motor 1 and disable motor 2.
To set the microstep mode of BOTH motor drivers (the same signals go to both drivers, so you can't set them separately) use a value of 1,2,3,4 or 5 for <Enable1>. When you use a value of 1,2,3,4 or 5 for <Enable1>, the <Enable2> parameter is not needed.
When setting microstep values with <Enable1>:
1 will enable both axis in 1/16th step mode (default on boot)
2 will enable both axis in 1/8th step mode
3 will enable both axis in 1/4 step mode
4 will enable both axis in 1/2 step mode
5 will enable both axis in full step mode
Note that any time an SM command is executed, both motors become 'enabled' before the move starts. Thus it is almost never necessary to issue a "EM,1,1" command to enable both motors.
Example: "EM,2" - this command will set both motors in 1/8th step mode
Example: "EM,0,0" - this command will disable both motors (they will then freewheel)
Example: "EM,1,1" - this command will enable both motors and set them to 1/16th microstep mode.
Return Packet: "OK"
```

### Using pyserial
I found my device ID by watching what changed in `/dev` when I plugged in the board.

```python
import serial
s = serial.Serial('/dev/cu.usbmodemfa141', 9600, timeout=1)
# step-mode is 1/16th by default and the EMSL steppers are 200 steps/rev so this is a full rev in 5000ms
ser.write('SM,5000,3200\r')

# then go to 1 step mode and make a single rev in 2000ms
ser.write('EM,5')   # the EM write seems to "eat" the next command.. still puzzling over this
ser.write('SM,2000,200\r')
```


### Maths
see if this makes sense:

```
   *                    *  (0,L)
    \                 /
     \              /
      \           /
   a   \        /   b
        \     /
         \  /
          o
            (x,y)
```

so 

```
  a = &radic;(x&sup2; + y&sup2;)

  b = &radic;(y&sup2; + (L-x)&sup2;)
```

also, with regard to the spinning steppers and our 200 steps per revolution, if ```s``` is the number of steps:

```
  &Delta;a = r&theta;
  &theta; = 2s&pi;/200
  &there4;
  s = 100&Delta;a/(r&pi;)
``` 

