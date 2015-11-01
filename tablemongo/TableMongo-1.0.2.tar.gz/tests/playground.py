from models import *

print(Trip.waypoints == Coordinate(1, 3))
print(Trip.waypoints != Coordinate(1, 3))
print(db.NOT(Trip.waypoints != Coordinate(1, 3)))

print('')

print((Trip.waypoints == Coordinate(1, 3)).bson(Trip))
print((Trip.waypoints != Coordinate(1, 3)).bson(Trip))
print(db.NOT(Trip.waypoints != Coordinate(1, 3)).bson(Trip))

print(db.AND(User.email < 5,  User.email > 7))