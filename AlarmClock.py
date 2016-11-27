import datetime

class AlarmClock():
	def __init__(self, alarm_time, time_difference=0, ring=True):
		# Le time (datetime.time)
		self.alarm_time = alarm_time
		# La difference, en minutes
		self.time_difference = time_difference
		self.ring = ring

	# N'essaie pas de comprendre cette fonction, je ne sais même pas pourquoi ça marche...
	def send_time(self):
		new_hour =  self.alarm_time.hour + (self.alarm_time.minute + self.time_difference)//60
		if new_hour >= 0  and new_hour <= 23:
			return datetime.time(new_hour, (self.alarm_time.minute + self.time_difference)%60).strftime("%H%M")
