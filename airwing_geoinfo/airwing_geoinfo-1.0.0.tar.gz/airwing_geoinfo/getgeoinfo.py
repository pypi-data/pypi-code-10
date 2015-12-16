import pycurl
import re
import StringIO

def getGeoinfo(workspaceUrl, user, name, data, GLOBAL_UNAME, GLOBAL_PWD):
	curl = pycurl.Curl()
	y = workspaceUrl + user + '/coveragestores/' + name + "/coverages/" + name + ".html"
	buf = StringIO.StringIO()
	curl.setopt(pycurl.WRITEFUNCTION, buf.write)
	curl.setopt(pycurl.URL, y)
	curl.setopt(pycurl.HTTPHEADER, ['Content-Type:application/json'])
	curl.setopt(pycurl.USERPWD, GLOBAL_UNAME + ":" + GLOBAL_PWD)
	curl.perform()
	thePage = buf.getvalue()
	reObj1 = re.compile('<li>[\s\S]*?</li>')
	if thePage[0:2] != '<!':
		print "Get geoinfo failed." + thePage
		return
	geoInfo = reObj1.findall(thePage)[-1].split('[')[-1].split(']')[0].split(',')
	longitute = geoInfo[0].split(':')
	latitude = geoInfo[-1].split(':')
	latitude[0] = latitude[0].strip()
	latitude[1] = latitude[1].strip()
	longitute[0] = longitute[0].strip()
	longitute[1] = longitute[1].strip()
	newgeoInfo = {
		'left_longitude':longitute[1],
		'left_latitude':latitude[1],
		'right_longitude':longitute[0],
		'right_latitude':latitude[0]
	}
	buf.close()
	return newgeoInfo