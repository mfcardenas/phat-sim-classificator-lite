"""
    Class Read Data Sensor I2c port on BeagleBone
    UCM
"""
import smbus
import time
 
bus = smbus.SMBus(1)
 
# ADXL345 device address
ADXL345_DEVICE = 0x53
 
# ADXL345 constants
EARTH_GRAVITY_MS2   = 9.80665
SCALE_MULTIPLIER    = 0.004
 
DATA_FORMAT         = 0x31
BW_RATE             = 0x2C
POWER_CTL           = 0x2D
 
BW_RATE_1600HZ      = 0x0F
BW_RATE_800HZ       = 0x0E
BW_RATE_400HZ       = 0x0D
BW_RATE_200HZ       = 0x0C
BW_RATE_100HZ       = 0x0B
BW_RATE_50HZ        = 0x0A
BW_RATE_25HZ        = 0x09
 
RANGE_2G            = 0x00
RANGE_4G            = 0x01
RANGE_8G            = 0x02
RANGE_16G           = 0x03
 
MEASURE             = 0x08
AXES_DATA           = 0x32
 
class ReadI2CPort:
    """ ReadI2CPort Class  """
    address = None
 
    def __init__(self, address = ADXL345_DEVICE):
        """ Init ReadI2CPort """
        self.address = address
        self.setBandwidthRate(BW_RATE_50HZ)
        self.setRange(RANGE_2G)
        self.enableMeasurement()
 
    def enableMeasurement(self):
        """ Enable Measurement """
        bus.write_byte_data(self.address, POWER_CTL, MEASURE)
 
    def setBandwidthRate(self, rate_flag):
        """ Set Banwidth Rate """
        bus.write_byte_data(self.address, BW_RATE, rate_flag)
 
    # set the measurement range for 10-bit readings
    def setRange(self, range_flag):
        """ Set Range """
        value = bus.read_byte_data(self.address, DATA_FORMAT)
 
        value &= ~0x0F
        value |= range_flag
        value |= 0x08
 
        bus.write_byte_data(self.address, DATA_FORMAT, value)
 
    # returns the current reading from the sensor for each axis
    #
    # parameter gforce:
    #    False (default): result is returned in m/s^2
    #    True           : result is returned in gs
    def getAxes(self, gforce = False):
        """ Get Axes Data for Sensor """
        bytes = bus.read_i2c_block_data(self.address, AXES_DATA, 6)
 
        x = bytes[0] | (bytes[1] << 8)
        if(x & (1 << 16 - 1)):
            x = x - (1<<16)
 
        y = bytes[2] | (bytes[3] << 8)
        if(y & (1 << 16 - 1)):
            y = y - (1<<16)
 
        z = bytes[4] | (bytes[5] << 8)
        if(z & (1 << 16 - 1)):
            z = z - (1<<16)
 
        x = x * SCALE_MULTIPLIER 
        y = y * SCALE_MULTIPLIER
        z = z * SCALE_MULTIPLIER
 
        if gforce == False:
            x = x * EARTH_GRAVITY_MS2
            y = y * EARTH_GRAVITY_MS2
            z = z * EARTH_GRAVITY_MS2
            
        x = round(x, 6)
        y = round(y, 6)
        z = round(z, 6)
 
        return {"timestamp": int(time.time()*1000), "x": x, "y": y, "z": z}
 
if __name__ == "__main__":
    adxl345 = ReadI2CPort()
    while True:
        axes = adxl345.getAxes(False)
        print ("timestamp = ", int(time.time()*1000), ", x = ", axes['x'], ", y = ", axes['y'], ", z = ", axes['z'], "")
        time.sleep(0.3)