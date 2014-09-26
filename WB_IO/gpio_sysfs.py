import threading
import select
from collections import defaultdict

IN = "in"
OUT = "out"
RISING = "rising"
FALLING = "falling"
BOTH = "both"
NONE = "none"

BOARD = "board"
BCM = "bcm"

HIGH = 1
LOW = 0


class GPIOHandler(object):
    def __init__(self):
        self.event_callbacks = {}
        self.gpio_fds = {}

        self.epoll = select.epoll()

        self.polling_thread = threading.Thread(target = self.gpio_polling_thread)
        self.polling_thread.daemon = True
        self.polling_thread.start()

        self.gpio_first_event_fired = defaultdict(lambda: False)

    def gpio_polling_thread(self):
        while True:
            events = self.epoll.poll()
            for fileno, event in events:
                for gpio, fd in self.gpio_fds.iteritems():
                    if fileno == fd.fileno():
                        if self.gpio_first_event_fired[gpio]:
                            #~ print "fire callback"
                            cb = self.event_callbacks.get(gpio)
                            if cb is not None:
                                cb(gpio)
                        else:
                            self.gpio_first_event_fired[gpio] = True


    def export(self, gpio):
        if not os.path.exists('/sys/class/gpio/gpio%d' % gpio):
            open('/sys/class/gpio/export','wt').write("%d\n" % gpio)

    def setup(self, gpio, direction):
        self.export(gpio)

        oldfd = self.gpio_fds.pop(gpio, None)
        if oldfd:
            oldfd.close()

        open('/sys/class/gpio/gpio%d/direction' % gpio, 'wt').write("%s\n" % direction)
        self._open(gpio)

    def _open(self, gpio):
        fd  = open('/sys/class/gpio/gpio%d/value' % gpio, 'r+')
        self.gpio_fds[gpio] = fd

    def _check_open(self, gpio):
        if gpio not in self.gpio_fds:
            self._open(gpio)



    def input(self, gpio):
        self._check_open(gpio)

        self.gpio_fds[gpio].seek(0)
        val= self.gpio_fds[gpio].read().strip()
        return False if val == '0' else True

    def output(self, gpio, value):
        self._check_open(gpio)

        self.gpio_fds[gpio].seek(0)
        self.gpio_fds[gpio].write('1' if value == self.HIGH else '0')



    def request_gpio_interrupt(self, gpio, edge):
        val = open('/sys/class/gpio/gpio%d/edge' % gpio, 'wt').write("%s\n" % edge)
        self._check_open(gpio)

    def add_event_detect(self, gpio, edge, callback):
        self.request_gpio_interrupt(gpio, edge)

        already_present = (gpio in self.event_callbacks)
        self.event_callbacks[gpio] = callback
        if not already_present:
            self.gpio_first_event_fired[gpio] = False
            self.epoll.register(self.gpio_fds[gpio], select.EPOLLIN | select.EPOLLET)

    def remove_event_detect(self, gpio):
        self.request_gpio_interrupt(gpio, self.NONE)
        ret = self.event_callbacks.pop(gpio, None)

        if ret is not None:
            self.epoll.unregister(self.gpio_fds[gpio])


    def wait_for_edge(self, gpio, edge):
        event = threading.Event()
        event.clear()
        callback = lambda x: event.set()

        self.add_event_detect(gpio, edge, callback)
        #~ print "wait for edge..."
        event.wait(1E100)
        #~ print "wait for edge done"
        self.remove_event_detect(gpio)

    def setmode(self, mode):
        raise NotImplementedError

    #~ self.irq_gpio, GPIO.RISING, callback=self.interruptHandler)
_gpio_handler = GPIOHandler()
wait_for_edge = _gpio_handler.wait_for_edge
export = _gpio_handler.export
setup = _gpio_handler.setup
input = _gpio_handler.input
output = _gpio_handler.output
add_event_detect = _gpio_handler.add_event_detect
remove_event_detect = _gpio_handler.remove_event_detect
wait_for_edge = _gpio_handler.wait_for_edge
setmode = _gpio_handler.setmode



