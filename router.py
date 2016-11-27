import tornado.ioloop
import tornado.web
from RatpWatcher import RatpWatcher
from WeatherWatcher import WeatherWatcher
from Application import Application
from AlarmClock import AlarmClock
from Criteria import Criteria



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("template.html", title="My title", items=items)

class AppCreator(tornado.web.RequestHandler):
    def get(self):
        app = Application()


        alarm_time = self.get_argument("alarm_time")
        country = self.get_argument("country")
        zip_code = self.get_argument("zip_code")
        city = self.get_argument("city")
        criteria_name = self.get_argument("criteria_name")
        criteria_args = self.get_argument("criteria_args")

        alarm_clock = AlarmClock(alarm_time)
        criteria = Criteria(criteria_name, criteria_args)

        app.set_country(country)
        app.set_zip_code(zip_code)
        app.set_city(city)
        app.set_alarm_clock(alarm_clock)
        app.set_criteria(criteria)

        app.startApplication(app.get_alarm_clock().get_alarm_time())

class RatpHandler(tornado.web.RequestHandler):
    def get(self,lines):
        rw = RatpWatcher(lines.split("-"))
        state = rw.ratpStatus()
        print(state)

class WeatherHandler(tornado.web.RequestHandler):
    def get(self,args):
        splittedArgs = args.split("-")  
        ww = WeatherWatcher(splittedArgs[0],application.getLatitude(),application.getLongitude(),splittedArgs[1], splittedArgs[2])
        state = ww.meteoStatus()
        print(state)

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