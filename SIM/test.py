from obu import Obu

def movement(lat, long):
    lat += 1
    long += 1
    return lat, long

obu1 = Obu("obu1")

print(obu1)
obu1.move(movement)
print(obu1)