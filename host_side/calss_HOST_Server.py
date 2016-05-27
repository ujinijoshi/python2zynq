#!usr/bin/python
#Author: IQ
#Purpose: Server to send all commands at port 8889

import socket
import time
import crcmod   #crc16 polynomial 0x18005, rev=True
import random
from random import randint  # generate hope array
import struct
from threading import Thread

HOST = '10.0.0.1'
HOST_PORT = 8889
AERO_PORT = 8890
AERO_IP = '10.0.0.3'
HOST_IP = '10.0.0.1'

num_timestamps = 1
num_hope_index = 5

# CRC-16 mod fucntion
crc16_func = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0x0000, xorOut=0x0000)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST,AERO_PORT))
# CRC-16 calculation,returns payload + CRC
def crc(payload): # payload should be a string
	#htons is used so that hex to asacii equivalent sent,and 2 bytes are packed
	return payload + struct.pack('H',socket.htons(crc16_func(payload)))

def hop_array():
	freq_array = ''
	for p in range(0,num_hope_index):
		freq_array += struct.pack('>H',randint(0,7))
		
	hope_rate = 5000
	Mode = 1  # 0=ED , 1=GPS
	
	#struct packing fmt '!B' means network endianess(big endn) '>' bigEnd '<' littleEnd
	freq_array = freq_array + struct.pack('>HB',hope_rate,Mode)

	return freq_array 	

def timestamp_array():
	print 'Timestamps Daemon started......\n'
	i = 1
	while True:
		time.sleep(1)
		timestamps = ''
		for t in range(0,num_timestamps):
			time_epoch = float(time.time()*1000000)
			timestamps += struct.pack('d',time_epoch)
			
		pkt_no = 14
		pkt_repeat_no = 5  # 0=ED , 1=GPS
		on_duratoin = 100
		
		if len(timestamps) % 8 != 0:
			print 'length is boguss: ', len(timestamps)
		else:	
			timestamps = struct.pack('BBH',pkt_no,pkt_repeat_no,on_duratoin) + timestamps
			frame_timestmps = '61'.decode('hex') + timestamps
			#print frame_timestmps
			payload = crc(frame_timestmps)
			#print len(payload[4:])
			s.sendto(payload,(AERO_IP,HOST_PORT))

		i +=1	
		#return timestamps	

def receive_daemon():
	#print 'Receive Daemon started...'
    while True:
        data, address = s.recvfrom(1024)  
        if not data:            
            continue
        print 'Frame - [Header:', data[0], 'value:', str(data[1:2]) ,' Address: ', str(address ), 'length: ', len(data)
     

class frame_generator(Thread):
	"""docstring for frame_generator"""
	def __init__(self, socket,frame_id):
		super(frame_generator, self).__init__()
		self.frame_id = frame_id
		self.s = socket
		
	def send(self,payload):
		self.s.sendto(payload,(AERO_IP,HOST_PORT))
			

	def receive(self):
			data, address = self.s.recvfrom(1024)		
			print 'Frame - [Header:', data[0], ' CRC: ', data[-4:] ,' Address: ', str(address ), 'length: ', len(data)
			
	def run(self):

		payload = crc(self.frame_id)		
		self.send(payload)
		#self.receive()

		
if __name__ == '__main__':

#Default Frame settings
	
	frame_request = struct.pack('BB',ord('50'.decode('hex')),1)
	frame_keepalive = struct.pack('BB',ord('52'.decode('hex')),1)  
	frame_Icf_Fixed = struct.pack('BB',ord('4C'.decode('hex')),0) 
	frame_Icf_conld = struct.pack('BB',ord('4C'.decode('hex')),1)
	frame_get_power = struct.pack('BB',ord('56'.decode('hex')),1) 
	frame_hope_aray = struct.pack('B',ord('4E'.decode('hex'))) + hop_array()
	#frame_timestmps = '61'.decode('hex') + timestamp_array()
	
	frame_list = [frame_request,
				  #frame_keepalive,
				  #frame_Icf_conld,
				  struct.pack('B',ord('4E'.decode('hex'))) + hop_array(),
				  #frame_get_power
				  ]
	
	
	t1 = Thread(target = receive_daemon)
	t1.setDaemon(True)
	t1.start()
	
	#timestamp_thread = Thread(target = timestamp_array)
	#timestamp_thread.setDaemon(True)
	#timestamp_thread.start()
	
	try:
		while True:
			raw_input('Press Enter to send connection request....! ')
			#print 'Server Sending request...'
			threads = []
			for frame in frame_list:
				#print frame
				t = frame_generator(s,frame)
				threads.append(t)
				t.start()
			for t in threads:
				t.join()
			#t1.join()
			time.sleep(0.5)
			print '\nThread complete'
	except Exception,e:
		pass

	finally:
		s.close()

		
	
	
		




