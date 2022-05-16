
class Obu:
    
    def __init__(self, name, lat=0, long=0):
        self.name = name
        self.lat = lat
        self.long = long

    def __repr__(self):
        return f'{self.name}: [ latitude: {self.lat}, longitude: {self.long} ]'

    def move(self, func):
        r = func(self.lat, self.long)
        self.lat = r[0]
        self.long = r[1]

