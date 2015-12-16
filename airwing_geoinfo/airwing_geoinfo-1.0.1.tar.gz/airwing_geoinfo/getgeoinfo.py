import requests

def getGeoinfo(service_url, user, name, data, geo_user, geo_pwd):
	s = requests.Session()
	data = {
		'username': geo_user,
		'password': geo_pwd
	}
	service_url = service_url.split('/rest')[0]
	s.post(service_url+'/j_spring_security_check', data=data, allow_redirects=False)
	y = service_url + '/rest/workspaces/' + user + '/coveragestores/' + name + "/coverages/" + name + ".json"
	geoinfo = s.get(y, allow_redirects=False).json()
	geoinfo = geoinfo['coverage']['latLonBoundingBox']
	print geoinfo['minx']
	newgeoInfo = {
		'left_longitude': geoinfo['minx'],
		'left_latitude': geoinfo['miny'],
		'right_longitude': geoinfo['maxx'],
		'right_latitude': geoinfo['maxy']
	}
	return newgeoInfo