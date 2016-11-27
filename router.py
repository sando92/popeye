import tornado.ioloop
import tornado.web
import datetime
from RatpWatcher import RatpWatcher
from WeatherWatcher import WeatherWatcher
from AlarmClock import AlarmClock
from Criteria import Criteria
from Application import Application


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("template.html", title="My title", items=items)

class AppCreator(tornado.web.RequestHandler):
    def get(self):
        #alarm_time = self.get_argument("alarm_time")
        #zip_code = self.get_argument("zip_code")
        #city = self.get_argument("city")
        #criteria_name = self.get_argument("criteria_name")
        #criteria_args = self.get_argument("criteria_args")

        #alarm_clock = AlarmClock(alarm_time)
        alarm_time = datetime.time(10, 59)

        #criteria = Criteria(criteria_name, criteria_args)

        App = Application()
        App.start_application(alarm_time)

class RatpHandler(tornado.web.RequestHandler):
    def get(self,lines):
        try:
            rw = RatpWatcher(lines.split("-"))
            state = rw.ratpStatus()
            print("Etat de la ligne {}".format(state))
            if state == 1:
                return self.write("-9")
            else:
                return self.write("0")
                #retirer 30 min à l'heure de l'alarme en passant par la classe AlarmClock
                #renvoyer HHMM au réveil

        except Exception:
            print("ERROR")

class WeatherHandler(tornado.web.RequestHandler):
    def get(self,args):
        try:
            splittedArgs = args.split("-")
            ww = WeatherWatcher(splittedArgs[0],application.getLatitude()
                ,application.getLongitude(),splittedArgs[1], splittedArgs[2])
            state = ww.meteoStatus()
            if state == 1:
                #we do not let the alarm clock ring
                requests.get("http://192.168.2.2/ALARMTIME=" + alarmClock.getAlarmTime())
        except Exception:
            print("ERROR")


def make_app():
    return tornado.web.Application([
        (r"/popeye", MainHandler),
        (r"/ratp/(.*)", RatpHandler),
        (r"/weather/(.*)", WeatherHandler),
        (r"/create/application/", AppCreator),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
