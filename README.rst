**PLEASE NOTE:  This library may have breaking changes as development continues.  Please read the changelog anytime you update the library!**

**The PWM Duty Cycle range was reversed in 0.0.15 from 100(off)-0(on) to 0(off)-100(on).  Please update your code accordingly.**

**Adafruit's BeagleBone IO Python Library**

This is a set of Python tools to allow GPIO, PWM, and ADC access on the BeagleBone using the Linux 3.8 Kernel and above (latest releases).

It has been tested on the 5-20 and 6-6 Angstrom image on the BeagleBone Black.

**Note: BBIO has been renamed to Adafruit_BBIO.**

**Installation on Angstrom**
::
    git clone git://github.com/contactless/wb-io-python.git 
    #set the date and time 
    /usr/bin/ntpdate -b -s -u pool.ntp.org 
    #install dependency 
    opkg update && opkg install python-distutils 
    cd wb-io-python 
    python setup.py install

**Installation on Ubuntu/Debian**
::
    sudo ntpdate pool.ntp.org
    sudo apt-get update
    sudo apt-get install build-essential python-dev python-pip -y
    git clone git://github.com/contactless/wb-io-python.git 
    cd wb-io-python
    sudo python setup.py install
    cd ..
    sudo rm -rf wb-io-python
    
**Usage**

Using the library is very similar to the excellent RPi.GPIO library used on the Raspberry Pi. Below are some examples.

**GPIO Setup** 

Import the library, and setup as GPIO.OUT or GPIO.IN::

    import WB_IO.GPIO as GPIO
    GPIO.setup(247, GPIO.OUT)

Here, 247 is a GPIO id for Relay 1 on Wiren Board Smart Home rev. 3.5. List of all GPIO id avaliable on http://contactless.ru/wiki

**GPIO Output** 

Setup the pin for output, and write GPIO.HIGH or GPIO.LOW. Or you can use 1 or 0.::

    import WB_IO.GPIO as GPIO
    GPIO.setup(247, GPIO.OUT) GPIO.output(247, GPIO.HIGH)
    
**GPIO Input**

Inputs work similarly to outputs.::

    import WB_IO.GPIO as GPIO
    GPIO.setup(id, GPIO.IN)
    
Polling inputs::
    
    if GPIO.input(id):
      print("HIGH")
    else:
      print("LOW")

Waiting for an edge (GPIO.RISING, GPIO.FALLING, or GPIO.BOTH::

    GPIO.wait_for_edge(channel, GPIO.RISING)

Detecting events::

    GPIO.add_event_detect(id, GPIO.FALLING) 
    #your amazing code here 
    #detect wherever: 
    if GPIO.event_detected(id):
      print "event detected!"

**PWM**::

    import WB_IO.PWM as PWM 
    #PWM.start(channel, duty, freq=2000, polarity=0) 
    #duty values are valid 0 (off) to 100 (on) 
    PWM.start(id, 50)
    PWM.set_duty_cycle(id, 25.5) 
    PWM.set_frequency(id, 10)

    PWM.stop(id)
    PWM.cleanup()
    
    #set polarity to 1 on start:
    PWM.start(id, 50, 2000, 1)

**ADC**::

    import WB_IO.ADC as ADC
    ADC.setup()

    #read returns values 0-1.0 
    value = ADC.read(id)

    #read_raw returns non-normalized value 
    value = ADC.read_raw(id)

**Running tests**

Install py.test to run the tests. You'll also need the python compiler package for py.test.::

    opkg update && opkg install python-compiler 
    #Either pip or easy_install 
    pip install -U pytest 
    easy_install -U pytest

Execute the following in the root of the project::

    py.test
    
**Credits**

The BeagleBone IO Python library was originally forked from the excellent MIT Licensed [RPi.GPIO](https://code.google.com/p/raspberry-gpio-python) library written by Ben Croston.

**License**

Written by Justin Cooper, Adafruit Industries. BeagleBone IO Python library is released under the MIT License.
