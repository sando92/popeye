import requests

from AlarmConfig import AlarmConfig


class WeatherWatcher():
    """Classe pour obtenir les informations sur la météo. Permet de désactiver ou non le réveil en cas de mauvaises conditions météorologiques."""

    def __init__(self, criteria, lattitude, longitude, limit, moreless):
        self.criteria = criteria
        self.lat = lattitude
        self.lon = longitude
        self.limit = limit
        self.moreless = moreless
        self.key = '499f075c29804a29895184718162611'
        self.status = None
        self.setStatus()

    def callApi(self, ):
        url = 'http://api.apixu.com/v1/current.json?q={lat},{lon}&key={key}'.format(lat=self.lat, lon=self.lon, key=self.key)
        return requests.post(url=url)

    def getIndicator(self):
        response_json = self.callApi().json()['current']
        if self.criteria == 'rain':
            indicator = response_json['precip_mm']
        elif self.criteria == 'wind':
            indicator = response_json['wind_kph']
        return indicator

    def setStatus(self):
        indicator = self.getIndicator()
        if self.moreless == 'more':
            if indicator >= self.limit:
                self.status = True
            else:
                self.status = False
        else:
            if indicator >= self.limit:
                self.status = False
            else:
                self.status = True

    def weatherStatus(self):
        return AlarmConfig(self.status)
