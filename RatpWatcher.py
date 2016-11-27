import requests
import json

from AlarmConfig import AlarmConfig


class RatpWatcher():
    def __init__(self, lines):
        if not isinstance(lines, list):
            if isinstance(lines, str):
                lines = [lines]
            else:
                raise Exception

        self.lines = lines

        # Initialisaiton of the request
        self.url = "http://www.ratp.fr/meteo/ajax/data"
        self.header = {
            'Host': 'www.ratp.fr',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4,es;q=0.2',
            'Cookie': 'xtvrn=$63370$; ratp=sstkb9l2nqcakb98ga1go37nv6; idm=1; xtan63370=-; xtant63370=1'
        }

        self.response = None
        self.problem = 0

        # Les types de keys possible
        self.lineTypes = ["tram", "metro", 'rer']

        # On rempli la réponse
        self.getRatpDatas()

    def callApi(self):
        self.response = requests.get(self.url, headers=self.header)

    def getRatpDatas(self):
        self.callApi()
        self.response = json.loads(str(self.response.content)[2:-1])

    def datas(self):
        return self.response

    def getLineStatus(self, lineType, lineNumber):
        if lineType in self.lineTypes:
            tmp = self.response['status'][lineType]["lines"][lineNumber]["name"]
            return tmp

    def ratpStatus(self):
        print("Datas récupérées à {}".format(self.response["now"]))
        if self.problem == 1:
            return AlarmConfig.add_time_diff(-30)
        for line in self.lines:
            splittedInfo = line.split("_")
            if self.getLineStatus(splittedInfo[0], splittedInfo[1]) != "normal":
                self.problem = 1
                return AlarmConfig.add_time_diff(-30)
        return AlarmConfig.no_changes()
