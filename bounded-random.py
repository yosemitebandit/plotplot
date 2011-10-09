'''
bounded-random
moves randomly within some bounds
'''
import math
import sys
import time
import serial
import random
    
s = serial.Serial(sys.argv[1], 9600, timeout=1)

# 3200 x 3200 drawing area (arbitrary)
motorSeparation = 3200
motorRadius = 26  # eric-units


def main():
    # start the pen in the middle roughly
    position = [1600, 1600]
    xBounds = [1400, 1800]
    yBounds = [1400, 1800]

    while(1):
        # get the current lengths of the strings
        leftLength = getLeftLength(position)
        rightLength = getRightLength(position)

        # generate a random new coordinate; save the old
        oldPosition = position
        position = [position[0] + random_delta(), position[1] + random_delta()]

        # check the bounds
        if position[0] < xBounds[0]:
            position[0] = xBounds[0]
        elif position[0] > xBounds[1]:
            position[0] = xBounds[1]

        if position[1] < yBounds[0]:
            position[1] = yBounds[0]
        elif position[1] > yBounds[1]:
            position[1] = yBounds[1]

        # determine how much each motor needs to move to achieve this distance
        leftDelta = leftLength - getLeftLength(position)
        rightDelta = rightLength - getRightLength(position)

        # generate random duration
        moveMotors(leftDelta, rightDelta, random_duration())

        print 'moving to %s' % position


def random_duration():
    return random.randint(3000, 4000)


def random_delta():
    delta = random.randint(50,200)
    if random.random() < 0.5:
        delta *= -1
    return delta


def computeSteps(delta):
    return 1600*delta/(motorRadius*math.pi)


def moveMotors(leftDelta, rightDelta, duration):
    ''' commands to the steppers
    '''
    leftSteps = int(computeSteps(leftDelta)) * -1
    rightSteps = int(computeSteps(rightDelta))
    command = 'SM,%d,%s,%s\r' % (duration, leftSteps, rightSteps)

    print 'executing %s' % command
    s.write(command)

    # hold up till we're done
    time.sleep(duration/1000. + 0.05)


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
