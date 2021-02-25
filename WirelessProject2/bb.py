import time

import pigpio

TRIGGER=18
ECHO=15

high_tick = None # global to hold high tick.

def cbfunc(gpio, level, tick):
    global high_tick
    if level == 0: # echo line changed from high to low.
        if high_tick is not None:
            echo = pigpio.tickDiff(high_tick, tick)
            cms = (echo / 1000000.0) * 34030 / 2
         #print("echo was {} micros long ({:.1f} cms)".format(echo, cms))
            print("%.0f" % cms)
    else:
        high_tick = tick

def main():
    pi = pigpio.pi() # Connect to local Pi.

    pi.set_mode(TRIGGER, pigpio.OUTPUT)
    pi.set_mode(ECHO, pigpio.INPUT)

    cb = pi.callback(ECHO, pigpio.EITHER_EDGE, cbfunc)

    start = time.time()

    #while (time.time()-start) < 60:
    pi.gpio_trigger(TRIGGER, 10)
    time.sleep(0.3)

    cb.cancel() # Cancel callback.
    pi.stop() # Close connection to Pi


if __name__=="__main__":
    main()
