bind = 'unix://${prefix}/var/run/adagucserver.socket'
workers = 2

# environment
raw_env = [
    "ADAGUC_CONFIG=${prefix}/etc/adagucserver/adaguc.autoresource.xml",
    "ADAGUC_LOGFILE=${prefix}/var/log/adaguc.log",
    "ADAGUC_DATARESTRICTION=FALSE",
    "PATH=${prefix}/bin:/usr/bin:/bin:/usr/local/bin",
    "GDAL_DATA=${prefix}/share/gdal",
    ]                                                                                                              

# logging
errorlog = '-'
accesslog = '-'
