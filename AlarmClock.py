import datetime

class AlarmClock():
	def __init__(self, alarm_time=None, time_difference=0, ring=True):
		# Le time (datetime.time)
		self.alarm_time = alarm_time
		# La difference, en minutes
		self.time_difference = time_difference
		self.ring = ring

	# Alarm Setter
	def set_alarm_time(self, alarm_time):
		self.alarm_time = alarm_time

	def get_alarm_time(self):
		return self.alarm_time

	# Time_Diff Setter
	def set_time_difference(self, time_diff):
		self.time_difference = time_diff

	def get_time_difference(self):
		return self.time_difference

	# Reset le décalage
	def reset_time_difference():
		self.time_difference = 0

	def must_ring(self):
        return self.ring

	# N'essaie pas de comprendre cette fonction, je ne sais même pas pourquoi ça marche...
	def to_arduino(self):
		# Test if the alarm is setted
		if not self.is_set():
			raise Exception("Alarm not setted")

		# Now we can calculate
		new_hour =  self.alarm_time.hour + (self.alarm_time.minute + self.time_difference)//60
		if new_hour >= 0  and new_hour <= 23:
			# Return to arduino timestamp
			return datetime.time(new_hour, (self.alarm_time.minute + self.time_difference)%60).strftime("%H%M")

	def is_set(self):
		return self.alarm_time is not None
