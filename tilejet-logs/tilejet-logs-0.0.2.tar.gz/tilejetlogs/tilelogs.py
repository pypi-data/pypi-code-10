def buildTileRequestDocument(tileorigin, tilesource, x, y, z, status, datetime, ip):
    r = {
        'ip': ip,
        'origin': tileorigin if tileorigin else "",
        'source': tilesource,
        'location': z+'/'+x+'/'+y,
        'z': z,
        'status': status,
        'year': datetime.strftime('%Y'),
        'month': datetime.strftime('%Y-%m'),
        'date': datetime.strftime('%Y-%m-%d'),
        'hour': datetime.strftime('%Y-%m-%d %H'),
        'minute': datetime.strftime('%Y-%m-%d %H:%M'),
        'date_iso': datetime.isoformat()
    }
    return r
