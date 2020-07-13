import pexpect
import sys
import struct
import math
import socket
import paho.mqtt.client as MQTT
import time

mqttclient = MQTT.Client(client_id='publisher_sensortag')
mqttclient.connect("127.0.0.1",1883)


def callback(t):
    x = t[0]+" : "+str(t[1])
    print x
    mqttclient.publish("sensors/health/gyro",t[1])
    time.sleep(2)
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((socket.gethostname(), 10000))
        client.send(x)
        from_serv = client.recv(4096)
        client.close()
        print('Received', from_serv)

    except:
        print "Server not available!!"


class SensorTag:
    data = {}

    sensors = {"imu": 0x57}

    @staticmethod
    def __round(t, decimal=2):
        "Round to specified decimal places."

        tmp = "{0:."+str(decimal)+"f}"
        if isinstance(t, tuple):
            return tuple([float(tmp.format(x)) for x in t])
        else:
            return float(tmp.format(t))

    class ConnectionFailure(Exception):
        '''
        Raised when a connection attempt fails, or an already established
                connection fails.
            You might need to press the side power button before attempting
            to connect. SensorTag has a green light blinking every second when
            it is in advertising mode.
        '''
        print "connection failed"

    def __init__(self, bluetooth_adr):
        self.con = pexpect.spawn('gatttool -b ' + bluetooth_adr + ' --interactive')
        self.con.expect('\[LE\]>', timeout=100)
        print ("Preparing to connect. You might need to press the side button...")
        self.con.sendline('connect')
        #self.con.expect('\[CON\].*>')
        return


    def char_write_cmd( self, handle, value ):
        # The 0%x for value is VERY naughty!  Fix this!
        cmd = 'char-write-cmd 0x%02x 0%x' % (handle, value)
        #print cmd
        self.con.sendline( cmd )
        return

    def char_read_hnd( self, handle ):
        self.con.sendline('char-read-hnd 0x%02x' % handle)
        self.con.expect('descriptor: .*? \r')
        after = self.con.after
        rval = after.split()[1:]
        return [long(float.fromhex(n)) for n in rval]

    def start(self, callback):
        """ Start the main notification loop.
        Callback is a fuction that gets a tuple, T
            T[0] = name of the sensor
            T[1] = processed value of a sensor
            T[2] = raw data received from the sensortag
        """
        #print "I am here!!"
        while True:
            try:
                pnum = self.con.expect('Notification handle = .*? \r', timeout=10)
            except pexpect.TIMEOUT:
                raise self.ConnectionFailure

            if pnum==0:
                after = self.con.after
                hxstr = after.split()[3:]
                handle = int(hxstr[0],16)
                #handle = long(float.fromhex(hxstr[0]))
                #print "handle", handle
                val = ''.join([chr(int(n,16)) for n in hxstr[2:]])
                #val = [long(float.fromhex(n)) for n in hxstr[2:]]
                #print "val", val
                # now lookup the kind of sensor this value belongs to, and
                #   call the appropriate _process_* routine. FIXME
                for s in self.sensors:
                    #print s, self.sensors[s]
                    if handle == self.sensors[s]:    # found it
                        func = getattr(self, "_process_"+s)
                        func(val)
                        #print s
                        #print "data", self.data[s]
                        callback((s, self.data[s]))
                        break

    def _process_temperature(self,v):

        def sensorTmp007Convert(t):
            SCALE_LSB = 0.03125
            return (t>>2) * SCALE_LSB

        objT, ambT = tuple([sensorTmp007Convert(t) for t in struct.unpack("<HH",v)])
        self.data["temperature"] = self.__round((objT, ambT))

    def _process_imu(self,v):

        def sensorMpu9250GyroConvert(data):
            return (data * 1.0) / (65536 / 500)

        def sensorMpu9250AccConvert(data):
            t = 8   ## FIXME
            return (data*1.0)/(32768.0/t)

        def sensorMpu9250MagConvert(data):
            return 1.0*data

        Gyro = tuple([sensorMpu9250GyroConvert(t) for t in struct.unpack("<hhh", v[0:6])])
        gyro_mag = 0
        for i in range(0, len(Gyro)):
            gyro_mag += Gyro[i]*Gyro[i]

        Gyro = math.sqrt(gyro_mag)

        #Accel = tuple([sensorMpu9250AccConvert(t) for t in struct.unpack("<hhh", v[6:12])])
        #Mag = tuple([sensorMpu9250MagConvert(t) for t in struct.unpack("<hhh", v[12:])])

        #self.data["imu"] = { "Gyro": self.__round(Gyro),
        #                     "Accelerometer": self.__round(Accel),
        #                     "Magnetometer": self.__round(Mag)}
        self.data["imu"] = self.__round(Gyro)

    def _process_humidity(self, v):

        def sensorHdc1000Convert(rawT, rawH):
            t = (rawT/65536.0)*165 - 40
            rh = (rawH/65536.0)*100
            return t, rh

        rawT, rawH = struct.unpack("<HH", v)
        t, rh = sensorHdc1000Convert(rawT, rawH)

        self.data["humidity"] = self.__round((t, rh))


    def _process_barometer(self, v):

        if len(v)==6:   # struct.unpack does not understand 24 bit integers
            t = (ord(v[2])<<16) + (ord(v[1])<<8) + ord(v[0])
            p = (ord(v[5])<<16) + (ord(v[4])<<8) + ord(v[3])
        else:
            t, p = struct.unpack("<HH", v)

        def calcBmp280(data):
            return data/100.0

        self.data["barometer"] = self.__round((calcBmp280(t), calcBmp280(p)))


    def _process_optical(self, v):

        rawLux = struct.unpack("<H", v)[0]

        def sensorOpt3001Convert(data):
            m, e = (data & 0x0FFF), ((data & 0xF000)>>12)
            return m * (0.01 * pow(2.0,e))

        self.data["optical"] = self.__round(sensorOpt3001Convert(rawLux))

def main():
    if len(sys.argv)<2:
        print "Usage: %s <bluetooth address>" ,sys.argv[0]
        sys.exit(1)

    bluetooth_adr = sys.argv[1]
    #sensors = ["temperature", "humidity", "barometer", "imu", "optical"]

    while True:
        print "Attempting to connect to", sys.argv[1]
        try:
            tag = SensorTag("BC:6A:29:C3:6F:26")
            """
            #temperature
            #tag.register_cb(0x25,tag._process_temperature)
            tag.char_write_cmd(0x29,0x01)
            tag.char_write_cmd(0x26,0x0100)

            #humidity
            #tag.register_cb(0x38,tag._process_temperature)
            tag.char_write_cmd(0x3c,0x01)
            tag.char_write_cmd(0x39,0x0100)

            #accelero
            tag.char_write_cmd(0x31,0x01)
            tag.char_write_cmd(0x2e,0x0100)

            #magneto
            tag.char_write_cmd(0x44,0x01)
            tag.char_write_cmd(0x41,0x0100)
            """

            #gyro
            tag.char_write_cmd(0x5b,0x07)
            tag.char_write_cmd(0x58,0x0100)
            """

            #barometer
            tag.char_write_cmd(0x4f,0x01)
            tag.char_write_cmd(0x4c,0x0100)
            """
            tag.start(callback)


        except SensorTag.ConnectionFailure:
            print("connection didnt happen!!")

if __name__ == "__main__":
    main()
