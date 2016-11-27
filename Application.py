import datetime

class Application():
	#alarm_clock cf. class, city, zip_code and country strings, criteria must be a dictionnary
	def __init__(self, alarm_clock=None, city=0, zip_code=0, criteria=None):
		self.alarm_clock = alarm_clock
		self.country = country
		self.city = city
		self.zip_code = zip_code
		self.criteria = criteria

	def startApplication(self):
		time = datetime.time.now()
		if (alarm_clock.alarm_time - time < 1heure)
			alarm_config = checkCriteria()
			setNewAlarmClock()

	def checkCriteria(self):
		alarm_config = AlarmConfig() #as to be set with the return of agregator
		#appel méthode de l'agregator pour connaitre la alarmClock config général des watchers

		return alarm_config

	def setNewAlarmClock(self):
		alarm_config = self.checkCriteria()

		self.alarm_clock.time_difference = alarm_config.time_difference
		self.alarm_clock.ring = alarm_config.ring
