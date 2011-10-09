'''
listener
takes keyboard chars (u-l-d-r) and moves the steppers up, left, down, or right
'''
import math
import sys
import time
import serial
    
s = serial.Serial(sys.argv[1], 9600, timeout=1)

# 3200 x 3200 drawing area (arbitrary)
motorSeparation = 3200
moveDistance = 100

# stepper config
motorDuration = 1000
motorRadius = 26

def main():
    # start the pen in the middle roughly
    position = [1600, 1600]
    while(1):
        direction = raw_input('specify a direction (udrl): ')
        # get the current lengths of the strings
        leftLength = getLeftLength(position)
        rightLength = getRightLength(position)

        # adjust the desired x,y coordinates of the pen head
        if direction == 'u':
            position = [position[0], position[1]-moveDistance]
        elif direction == 'd':
            position = [position[0], position[1]+moveDistance]
        elif direction == 'r':
            position = [position[0]+moveDistance, position[1]]
        elif direction == 'l':
            position = [position[0]-moveDistance, position[1]]

        # determine how much each motor needs to move to achieve this distance
        leftDelta = leftLength - getLeftLength(position)
        rightDelta = rightLength - getRightLength(position)

        print 'leftDelta %d' % leftDelta
        print 'rightDelta %d' % rightDelta

        moveMotors(leftDelta, rightDelta)

        print 'moving to %s' % position

    
def computeSteps(delta):
    return 1600*delta/(motorRadius*math.pi)


def moveMotors(leftDelta, rightDelta):
    ''' commands to the steppers
    '''
    leftSteps = int(computeSteps(leftDelta)) * -1
    rightSteps = int(computeSteps(rightDelta))
    command = 'SM,%d,%s,%s\r' % (motorDuration, leftSteps, rightSteps)

    print command
    s.write(command)

    # hold up till we're done
    time.sleep(motorDuration/1000)


def getLeftLength(position):
    ''' see trig in the readme
    '''
    return math.sqrt(position[0]**2 + position[1]**2)


def getRightLength(position):
    ''' see trig in the readme
    '''
    return math.sqrt(position[1]**2 + (motorSeparation - position[0])**2)


if __name__ == '__main__':
    main()
