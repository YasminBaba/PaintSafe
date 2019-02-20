#import necessary libraries
import smbus
import time

#create an smbus instance
bus = smbus.SMBus(1)


def sensor_setup():
	#CCS811 address is 0x5b
	#returns list of bytes in status register
	emptylist = []
    bus.write_i2c_block_data(0x5b,0xF4,emptylist)
	bus.sleep(0.2)
    status = bus.read_i2c_block_data(0x5b,0x00,1)
	#if status register 0d144 = 0b1001 0000, in application mode and valid application firmware is loaded
	if status == [144]:
		print("In application mode")
	#if status register 0d152 = 0b1001 1000, new data sample in ALG_RESULT_DATA (reg 0x02)
	elif status == [152]:
		print("In application mode, a new data sample is ready");
	else:
		print("Sensor setup not successful")
		
	return;
	
def measurement_mode():
	#sets sensor in mode 1, IAQ measurement every 1s
    modelist = [0b00010000]
    bus.write_i2c_block_data(0x5b,0x01,modelist)
	mode = bus.read_i2c_block_data(0x5b,0x01,1)
	if mode == [16]:
		print("In measurement mode")
	else:
		print("Failed to set to desired mode (Mode 1)")
	
	return;
	
sensor_setup()

measurement_mode()