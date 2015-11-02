from models import *

print(Trip().kind())
print(Trip.properties())
print(Trip.properties()[0].type())
print(Trip.waypoints.kind())
print(Trip.mro())
print(Trip.__mro__)