import serial, serial.tools.list_ports

class Arduino(object):
    """ Class that handles acquiring the serial data
        from the arduino for Data Acquisiton
    """

    def __init__(self, baud):
        usbport = self.get_serial()
        self.ser = serial.Serial(
             port=usbport,
             baudrate=baud,
             bytesize=serial.EIGHTBITS,
             parity=serial.PARITY_NONE,
             stopbits=serial.STOPBITS_ONE,
             timeout=1,
             xonxoff=0,
             rtscts=0,
             interCharTimeout=None
            )

    def get_serial(self):
        arduino_ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if 'Arduino' in p.description or 'USB Serial' in p.description
        ]
        if not arduino_ports:
            raise IOError("No Arduino found")
        else:
            usbport = arduino_ports[0]
        return usbport

    def poll(self):
        self.ser.flush() #flush before sending signal
        self.ser.write('w') #send signal telling Arduino to send data

        # now read all lines sent by the Arduino
        data = []

        # read analog channels
        for i in range(0,5+1): # now read the 6 analog channel
            data.append( int(self.ser.readline()[0:-2]) ) #this line will crash when running "test" because it sends strings not ints

        return data
