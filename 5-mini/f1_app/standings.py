import requests


class StandingsFetcher:
    DRIVER_URL = 'http://ergast.com/api/f1/current/driverStandings.json'
    CONSTRUCTOR_URL = 'http://ergast.com/api/f1/current/constructorStandings.json'

    def __init__(self, timeout=8):
        self.timeout = timeout
        self.session = requests.Session()
    self.last_error = None
    self.last_fetch = None

    def fetch(self):
        import time as _time
        out = {}
        self.last_error = None
        self.last_fetch = _time.time()
        try:
            drv = self.session.get(self.DRIVER_URL, timeout=self.timeout).json()
            cons = self.session.get(self.CONSTRUCTOR_URL, timeout=self.timeout).json()
            out['drivers'] = drv['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
            out['constructors'] = cons['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
        except Exception:
            import traceback
            try:
                self.last_error = traceback.format_exc()
            except Exception:
                self.last_error = 'error'
            out['drivers'] = []
            out['constructors'] = []
        return out
