import tornado.ioloop
import tornado.web
from RatpWatcher import RatpWatcher
from meteoWatcher

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("PopEye, l'optimisateur de sommeil ! ")

class RatpHandler(tornado.web.RequestHandler):
	def get(self,line):
		try:
            rw = RatpWatcher(line)
            problem=rw.ratpStatus()
            print(problem)
            if problem==1:
                #retirer 30 min à l'heure de l'alarme
                #renvoyer timestamp au réveil
                requests.get("http://192.168.2.2/ALARMTIME=0200")
		except Exception:
			print("ERROR")


def make_app():
    return tornado.web.Application([
        (r"/popeye", MainHandler),
        (r"/metro/(.*)", RatpHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()