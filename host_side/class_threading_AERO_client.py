#!usr/bin/python
#Author: IQ
#Purpose: Loopback Socket testing of general requests to port 8889

import socket
import random
from array import array
import struct
import threading
import thread
import crcmod   #crc16 polynomial 0x18005, rev=True
import time
import py2pl
#from pdb import *
HOST = '10.0.0.1'
HOST_PORT = 8889
AERO_PORT = 8890
AERO_IP = '10.0.0.3'
HOST_IP = '10.0.0.1'

CONNECTION_FLAG = 0
data = 0


def connect(value):
		global CONNECTION_FLAG 		
		if CONNECTION_FLAG == 0:
			print 'Connection request received!: '
			CONNECTION_FLAG = 1
			py2pl.push(4)
			return 1 		
		elif CONNECTION_FLAG == 1:
			print 'Connected! :'
			CONNECTION_FLAG = 2
			py2pl.push(8)
			return 2		
		elif CONNECTION_FLAG == 2:
			print 'Connection Already Established! :'
			return 2

def i_configure(value):
		print 'value: ', repr(value)
		Mode = struct.unpack('B',value)[0]
		if Mode == 0:
			print '-----Fixed Frequency Control------'
		if Mode == 1:
			print '----Dynamic Frequency Control-----'

def crc(payload): # CRC-16 calculation,returns payload + CRC
	#htons is used so that hex to asacii equivalent sent,and 2 bytes are packed
	return payload + struct.pack('H',socket.htons(crc16_func(payload)))

def hop_array(payload):
	#print payload
	freq_array = payload[:len(payload)-3]
	freq_array_decoded = 0
	# set the buffer frequency index values on FPGA
	
	#for t in range(0,len(freq_array)/2):
			
	#		freq_array_decoded = struct.unpack('>H',freq_array[t:t+2])[0]
	#		if t % 2 != 0:
	#			pass#print 'Frequency Hop Array' ,[t] , freq_array_decoded
	#		else:
	#			freq_array_decoded+=freq_array_decoded
	freq_array_decoded = array("H",freq_array)
	print freq_array_decoded
	freq_array_decoded.byteswap()
	print freq_array_decoded
	#freq_array_decoded.tolist()
	#import pdb; pdb.set_trace()
	hope_rate,Mode = struct.unpack('>HB',payload[-3:])
	#print freq_array.tolist(), 'Rate: ', hope_rate, 'Mode:  ', Mode
	print  'Rate: ', hope_rate, 'Mode:  ', Mode
	
	freq_list = freq_array_decoded.tolist()
	#print freq_list	
	py2pl.pushlist(freq_list)
	
	def alive(value):
	 #print 'alive'
	 pass
def send_power():
	tx_pwr_upper = 15
	rf_pwr_upper = 14
	tx_pwr_lower = 13
	rf_pwr_lower = 12
				
	#return struct.pack('>HHHH',tx_pwr_upper,rf_pwr_upper,tx_pwr_lower,rf_pwr_lower)	
	return struct.pack('>HH',tx_pwr_upper,rf_pwr_upper)	

def set_pa_timestamps(payload):
 			
	pkt_no,pkt_repeat_no,on_duratoin = struct.unpack('>BBH',payload[0:4])
	#print 'pkt_no: ', pkt_no, 'pkt_repeat_no:  ', pkt_repeat_no, 'On_duration: ',on_duratoin
	if len(payload[4:]) % 8 != 0:
			print 'length is boguss'
	else:	
		print 'PTSLength:', len(payload[4:])
		#Timestamps_array = array('d',payload[4:]) # set the buffer timestamps on FPGA
		#print Timestamps_array[0:3]
		#print time.time()
		time_array = payload[4:]
		#print time_array[0:8]

		for t in range(0,len(time_array)/8):
			
			time_array_decoded = struct.unpack('>Q',time_array[t:t+8])[0]
			
			if t % 8 != 0:
				pass#print 'Frequency Hop Array' ,[t] , freq_array_decoded
			else:
				print 'Timestamps Array' ,[t] , time_array_decoded


class frame_decoder(threading.Thread):
	def __init__(self,header,value):

		threading.Thread.__init__(self)
		self.header = header
		self.value = value

	def run(self):
		
		print "%s: %s" % (self.name, self.header)
		lock.acquire()
		if self.header == 'P': # 50 connection request
			status = connect(self.value) 
			#print 'connecting! '
			#message = ''.join(['Q',status.decode('hex')])
			message = struct.pack('BB',ord('51'.decode('hex')),status)
			payload = crc(message)
			s.sendto(payload,(HOST,AERO_PORT))

		elif self.header == 'L': # 4C initial configuration
			print ' Initial configuration! '		
			i_configure(self.value) 
			#s.sendto('4D01'.decode('hex'),(HOST,AERO_PORT))
			message = struct.pack('BB',ord('4D'.decode('hex')),1)
			payload = crc(message)
			s.sendto(payload,(HOST,AERO_PORT))

		elif self.header == 'N': # 4E sending hope array
			hop_array(self.value) 
			print ' setting Hoping Sequence! '
			#s.sendto('4F01'.decode('hex'),(HOST,AERO_PORT))
			message = struct.pack('BB',ord('4F'.decode('hex')),1)
			payload = crc(message)
			s.sendto(payload,(HOST,AERO_PORT))
		
		elif self.header == 'a': # 61 Set PA Timestamps 
			#pkt_info = set_pa(data) 
			print 'Setting PA Time Stamps! '
			#lock.acquire()
			#import pdb; pdb.set_trace()
			pkt_num,pkt_repeat,on_duratoin = struct.unpack('>BBH',self.value[0:4])

			set_pa_timestamps(self.value)
			message = struct.pack('>BBB',ord('62'.decode('hex')),pkt_num,pkt_repeat)
			payload = crc(message)
			s.sendto(payload,(HOST,AERO_PORT))
			#lock.release()	

		elif self.header == 'R': # 52 keep alive
			alive(self.value) 
			print ' >>>>Alive! '
			#s.sendto('5301',(HOST,AERO_PORT))
			message = struct.pack('BB',ord('53'.decode('hex')),1)
			payload = crc(message)
			s.sendto(payload,(HOST,AERO_PORT))

		elif self.header == 'T': # 54 change frequency
			#chang_freq(self.value) 
			print ' Change frequency ! '
			s.sendto('5501',(HOST,AERO_PORT))
		elif self.header == 'V': # 56 Get power
			power = send_power() 
			print 'Sending Power! '
			message = struct.pack('B',ord('57'.decode('hex'))) + power
			payload = crc(message)
			s.sendto(payload,(HOST,AERO_PORT))
		elif self.header == 'X': # 58 Get RSSI
			#rssi = send_rssi(data) 
			#print 'Sending RSSI! '
			s.sendto('5901RSSI',(HOST,AERO_PORT))
		elif self.header == '[': # 5D Log Read
			#logdata = log_read(data) 
			print 'sending Log time,freq,power,rssi,vswr,txrx! '
			s.sendto('5E01logdata',(HOST,AERO_PORT))
		elif self.header == '_': # 5F Set XY
			#ytime = set_xy(data) 
			print 'Setting XY ! '
			s.sendto('6501ytime',(HOST,AERO_PORT))
		
		elif self.header == 'c': # 63 Set TX Power
			#send_rssi(data) 
			print 'Setting TX Power! '
			#s.sendto('6401',(HOST,AERO_PORT))
		elif self.header == 'f': # 66 Set RSSI Threshold
			#set_rssithreshold(data) 
			print 'Setting RSSI Threshold! '
			s.sendto('6701',(HOST,AERO_PORT))
		elif self.header == 'X': # 68 Set Log difference
			#set_log_diff(data) 
			print 'Setting Log difference! '
			s.sendto('6901',(HOST,AERO_PORT))
		lock.release()	

	


if __name__ == '__main__':
	# CRC-16 mod fucntion
	crc16_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0x0000, xorOut=0x0000)

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((AERO_IP,HOST_PORT))

	#timestamp_thread = Thread(target = timestamp_array)
	#timestamp_thread.setDaemon(True)
	#timestamp_thread.start()

	print 'Client ready for connection at port 8889.....'
	
	while True:
		#5001 c0fd
		data, address = s.recvfrom(1024)
		if data[0] == 'P': # 50 connection request
				status = connect(data[1]) 
				message = struct.pack('BB',ord('51'.decode('hex')),status)
				payload = crc(message)
				s.sendto(payload,(HOST,AERO_PORT))
				break
		else: 
			print 'Please send connection request'		

	lock = threading.Lock()		
			
	try:
		
		while True:
			
			data, address = s.recvfrom(1024)
			#import pdb; pdb.set_trace()
			print 'Frame Received...   : ',data[0],'length: ', len(data) 
			#header_decoder(data[0],data[1:len(data)-4]) # data[0]--> header | data[1]-->self.value
			obj = frame_decoder(data[0],data[1:len(data)-2])
			obj.start()
			#T = threading.Thread(target = frame_decoder, args = (ata[0],data[1:len(data)-4]))
			#T.setDaemon(True)
			#T.start()
			#print 'Message[' + address[0] + ':' + str(address[1]) + '] - ' + data.strip()
	

	except Exception,e: 
		print str(e)


	finally:
		s.close()




