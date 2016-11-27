import tornado.ioloop
import tornado.web
from RatpWatcher import RatpWatcher
from WeatherWatcher import WeatherWatcher



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("template.html", title="My title", items=items)

class AlarmClockCreator(tornado.web.RequestHandler)
    def get(self):

class RatpHandler(tornado.web.RequestHandler):
	def get(self,lines):
		try:
            rw = RatpWatcher(lines.split("-"))
            state = rw.ratpStatus()
            print(state)
            if state == 1:
                #retirer 30 min à l'heure de l'alarme en passant par la classe AlarmClock 
                #renvoyer HHMM au réveil
                requests.get("http://192.168.2.2/ALARMTIME=" + alarmClock.getAlarmTime())
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
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()