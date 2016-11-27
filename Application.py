import datetime
import requests
import time as tt
from threading import Thread
from RatpWatcher import RatpWatcher
from WeatherWatcher import WeatherWatcher
from AlarmClock import AlarmClock
from Criteria import Criteria

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Application(metaclass=Singleton):
    def __init__(self):
        self.alarm_clock = AlarmClock()
        self.criteria = Criteria()
        self.country = None
        self.zip_code = None
        self.city = None

    def set_country(self,country):
    	self.country = country

    def set_zip_code(self, zip_code):
    	self.zip_code = zip_code

    def set_city(self, city):
    	self.city = city

    def set_criteria(self,criteria):
        self.criteria.set_name(criteria.get_name())
        self.criteria.set_args(criteria.get_args())

    def set_alarm_clock(self, alarm_clock):
        self.alarm_clock.set_alarm_time(alarm_clock.get_alarm_time())

    def functionToExec(self, hour, minu, delay):
        app = Application()
        a = datetime.datetime.now()
        b = datetime.datetime(2016, 11, 27, hour, minu-delay)
        c = b-a
        tt.sleep(c.seconds)
        resp = requests.get("http://localhost:8888/ratp/ligne_9")
        ac = AlarmClock(datetime.time(hour, minu), int(resp.content))
        print("http://192.168.2.2/ALARMTIME=" + ac.to_arduino())
        requests.get("http://192.168.2.2/ALARMTIME=" + ac.to_arduino())

    def start_application(self, alarm_time):
        hour = alarm_time.hour
        minute = alarm_time.minute
        t = Thread(target=self.functionToExec, args=[hour, minute, 1])
        t.start()

    def set_new_alarm_clock(self, alarm_config):
        self.alarm_clock.time_difference = alarm_config.time_difference
        self.alarm_clock.ring = alarm_config.ring
