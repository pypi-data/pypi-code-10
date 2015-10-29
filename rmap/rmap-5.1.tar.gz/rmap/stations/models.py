#from django.core import urlresolvers
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy

from django.db.models import permalink
from django.db.models import Q

from  django import VERSION as djversion
from rmap.utils import nint

if ((djversion[0] == 1 and djversion[1] >= 3) or 
    djversion[0] > 1):

    from django.db import models
    from django.db.models import signals

    class DeletingFileField(models.FileField):
        """
        FileField subclass that deletes the refernced file when the model object
        itself is deleted.
        
        WARNING: Be careful using this class - it can cause data loss! This class
        makes at attempt to see if the file's referenced elsewhere, but it can get
        it wrong in any number of cases.
        """
        def contribute_to_class(self, cls, name):
            super(DeletingFileField, self).contribute_to_class(cls, name)
            signals.post_delete.connect(self.delete_file, sender=cls)
        
        def delete_file(self, instance, sender, **kwargs):
            file = getattr(instance, self.attname)
            # If no other object of this type references the file,
            # and it's not the default value for future objects,
            # delete it from the backend.
            
            if file and file.name != self.default and \
                    not sender._default_manager.filter(**{self.name: file.name}):
                file.delete(save=False)
            elif file:
                # Otherwise, just close the file, so it doesn't tie up resources.
                file.close()

else:
    DeletingFileField=models.FileField



class SensorManager(models.Manager):
    def get_by_natural_key(self, name, board):
        #print "SensorManager: ",name,board
        return self.get(name=name, board=Board.objects.get_by_natural_key(board[0],board[1]))

class Sensor(models.Model):
    """Sensor driver metadata."""

    objects = SensorManager()

    SENSOR_DRIVER_CHOICES = (
        ('I2C',  'I2C drivers'),
        ('RF24',  'RF24 Network jsonrpc'),
        ('JRPC',  'INDIRECT jsonrpc over some transport'),
    )

    SENSOR_TYPE_CHOICES = (
        ('TMP',  'I2C TMP temperature sensor'),
        ('ADT',  'I2C ADT temperature sensor'),
        ('BMP',  'I2C BMP085/BMP180 pressure sensor'),
        ('HIH',  'I2C HIH6100 series humidity sensor'),
        ('DW1',  'I2C Davis wind direction and intensity adapter'),
        ('TBR',  'I2C Tipping bucket rain gauge adapter'),
        ('RF24', 'RF24 Network jsonrpc'),
    )

    active = models.BooleanField(ugettext_lazy("Active"),default=False,null=False,blank=False,help_text=ugettext_lazy("Activate this sensor to take measurements"))
    name = models.CharField(max_length=50,default="my sensor",blank=False,help_text=ugettext_lazy("Descriptive text"))

    driver = models.CharField(max_length=4,default="TMP",null=False,blank=False,choices=SENSOR_DRIVER_CHOICES,help_text=ugettext_lazy("Driver to use"))
    type = models.CharField(max_length=4,default="TMP",null=False,blank=False,choices=SENSOR_TYPE_CHOICES,help_text=ugettext_lazy("Type of sensor"))
    i2cbus=models.PositiveIntegerField(default=1,null=False,blank=True,help_text=ugettext_lazy("I2C bus number (for raspberry only)"))
    address=models.PositiveIntegerField(default=72,null=False,blank=False,help_text=ugettext_lazy("I2C ddress (decimal)"))
    node=models.PositiveIntegerField(default=1,blank=True,help_text=ugettext_lazy("RF24Network node ddress"))

    timerange = models.CharField(max_length=50,unique=False,default="254,0,0",null=False,blank=False,help_text=ugettext_lazy("Sensor metadata from rmap RFC"))
    level = models.CharField(max_length=50,unique=False,default="103,2000,-,-",null=False,blank=False,help_text=ugettext_lazy("Sensor metadata from rmap RFC"))

    board = models.ForeignKey('Board')

    def underscored_timerange(self):
        return self.timerange.replace(',','_')

    def underscored_level(self):
        return self.level.replace(',','_')

    def natural_key(self):
        #print "natural key sensor"
        #print self,self.name, self.board.natural_key()
        return (self.name, self.board.natural_key())

    natural_key.dependencies = ['stations.board']

#    def validate_unique(self, *args, **kwargs):
#        super(Sensor, self).validate_unique(*args, **kwargs)
#        if not self.id:
#            if self.__class__.objects.filter(name=name,board=board).exists():
#                raise ValidationError(
#                    {
#                        NON_FIELD_ERRORS: [
#                            'Sensor with same name already exists for this board.',
#                        ],
#                    }
#                )

    class Meta:
        ordering = ['driver']
        verbose_name = 'Sensor' 
        verbose_name_plural = 'Sensors' 
        # TODO unique will be unique for each timerange, level, station !
        unique_together = (('name', 'board'),)

    def __unicode__(self):
        #return u'%s-%s-%s-%s-%d-%s-%s-%s' % (self.name,self.active,self.driver,self.type,self.address,self.timerange,self.level,self.board)
        return u'%s-%s-%s' % (self.name,self.active,self.driver)

class TransportRF24NetworkManager(models.Manager):
    def get_by_natural_key(self, board):
        #print "TransportRF24NetworkManager:",board
        return self.get(board=Board.objects.get_by_natural_key(board[0],board[1]))

class TransportRF24Network(models.Model):
    """RF24 Network transport."""

    objects = TransportRF24NetworkManager()

    RF24_NODE_CHOICES = (
        (0,  'RF24 Network node 0'),
        (1,  'RF24 Network node 01'),
        (2,  'RF24 Network node 02'),
        (3,  'RF24 Network node 03'),
        (4,  'RF24 Network node 04'),
        (5,  'RF24 Network node 05'),
    )

    RF24_CHANNEL_CHOICES = (
        (90,  'RF24 Network node channel 90'),
        (91,  'RF24 Network node channel 91'),
        (92,  'RF24 Network node channel 92'),
        (93,  'RF24 Network node channel 93'),
        (94,  'RF24 Network node channel 94'),
        (95,  'RF24 Network node channel 95'),
    )

    RF24_KEYIV_CHOICES= (
        ("0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15",  'preset 1'),
        ("0,1,1,3,4,5,6,7,8,9,10,11,12,13,14,15",  'preset 2'),
        ("0,1,2,1,4,5,6,7,8,9,10,11,12,13,14,15",  'preset 3'),
        ("0,1,2,3,1,5,6,7,8,9,10,11,12,13,14,15",  'preset 4'),
        ("0,1,2,3,4,1,6,7,8,9,10,11,12,13,14,15",  'preset 5'),
        ("0,1,2,3,4,5,1,7,8,9,10,11,12,13,14,15",  'preset 6'),
        ("0,1,2,3,4,5,6,1,8,9,10,11,12,13,14,15",  'preset 7'),
        ("0,1,2,3,4,5,6,7,1,9,10,11,12,13,14,15",  'preset 8'),
        ("0,1,2,3,4,5,6,7,8,1,10,11,12,13,14,15",  'preset 9'),
    )

    active = models.BooleanField(ugettext_lazy("Active"),default=False,null=False,blank=False,help_text=ugettext_lazy("Activate this transport for measurements"))
    node = models.PositiveIntegerField(unique=False,default=0, choices=RF24_NODE_CHOICES,help_text=ugettext_lazy("Node ID for RF24 Network"))
    channel=models.PositiveIntegerField(default=93,null=False,blank=False, choices=RF24_CHANNEL_CHOICES,help_text=ugettext_lazy("Channel number for RF24"))

    #  TODO integer field to be converted to 0X
    key=models.CommaSeparatedIntegerField(max_length=47,null=False,blank=True, choices=RF24_KEYIV_CHOICES,help_text=ugettext_lazy("AES key"))
    iv=models.CommaSeparatedIntegerField(max_length=47,null=False,blank=True, choices=RF24_KEYIV_CHOICES,help_text=ugettext_lazy("AES cbc iv"))

    board = models.OneToOneField("Board")

    def natural_key(self):
        #print "natural key TransportRF24Network"
        #print self,self.board.natural_key()
        return (self.board.natural_key(),)

    natural_key.dependencies = ['stations.board']

    class Meta:
        ordering = ['node']
        verbose_name = 'RF24 Network node' 
        verbose_name_plural = 'RF24 Network nodes' 

    def __unicode__(self):
        return u'%s' % (self.node)


class TransportMqttManager(models.Manager):
    def get_by_natural_key(self, board):
        #print "TransportMqttManager: ",board
        return self.get( board=Board.objects.get_by_natural_key(board[0],board[1]))


class TransportMqtt(models.Model):
    """MQTT transport."""

    objects = TransportMqttManager()

    active = models.BooleanField(ugettext_lazy("Active"),default=False,help_text=ugettext_lazy("Activate this transport for measurements"))

    mqttsampletime = models.PositiveIntegerField(default=5,null=False,blank=False,help_text=ugettext_lazy("interval in seconds for publish"))
    mqttserver = models.CharField(max_length=50,default="mqttserver",null=False,blank=False,help_text=ugettext_lazy("MQTT server"))
    mqttuser= models.CharField(max_length=9,default="",null=False,blank=True,help_text=ugettext_lazy("MQTT user"))
    mqttpassword= models.CharField(max_length=50,default="",null=False,blank=True,help_text=ugettext_lazy("MQTT password"))

    board = models.OneToOneField("Board")

    def natural_key(self):
        #print "natural key"
        #print self,self.board.natural_key()
        return (self.board.natural_key(),)

    natural_key.dependencies = ['stations.board']

    class Meta:
        ordering = ['mqttserver']
        verbose_name = 'MQTT transport'
        verbose_name_plural = 'MQTT transport'

    def __unicode__(self):
        return u'%s' % (self.mqttserver)


class TransportTcpipManager(models.Manager):
    def get_by_natural_key(self, board):
        #print "TransportTcpipManager: ",board
        return self.get(board=Board.objects.get_by_natural_key(board[0],board[1]))

class TransportTcpip(models.Model):
    """TCP/IP transport."""

    objects = TransportTcpipManager()

    TCPIP_NAME_CHOICES = (
        ('master',   'master board 1'),
        ('master2',  'master board 2'),
        ('master3',  'master board 3'),
        ('master4',  'master board 4'),
    )

    mac={
        'master': (0,0,0,0,0,1) ,
        'master2':(0,0,0,0,0,2),
        'master3':(0,0,0,0,0,3),
        'master4':(0,0,0,0,0,4),
        'master4':(0,0,0,0,0,4),
    }

    active = models.BooleanField(ugettext_lazy("Active"),default=False,help_text=ugettext_lazy("Activate this transport for measurements"))
    name = models.CharField(max_length=50, default="master",blank=False,choices=TCPIP_NAME_CHOICES,help_text=ugettext_lazy("Name DSN solved (for master board only)"))

    ntpserver = models.CharField(max_length=50,default="ntpserver",null=False,blank=False,help_text=ugettext_lazy("Network time server (NTP)"))

    board = models.OneToOneField("Board")

    def natural_key(self):
        #print "natural key"
        #print self,self.board.natural_key()
        return (self.board.natural_key(),)

    natural_key.dependencies = ['stations.board']

    class Meta:
        ordering = ['name']
        verbose_name = 'tcp/ip DNS resoved name' 
        verbose_name_plural = 'tcp/ip DNS resoved names' 

    def __unicode__(self):
        return u'%s' % (self.name)

class TransportSerialManager(models.Manager):
    def get_by_natural_key(self, board):
        #print "TransportSerialManager:", board
        return self.get(board=Board.objects.get_by_natural_key(board[0],board[1]))

class TransportSerial(models.Model):
    """Serial transport."""

    objects = TransportSerialManager()

    SERIAL_BAUDRATE_CHOICES = (
        (9600,   '9600'),
        (19200,  '19200'),
        (38400,  '38400'),
        (11520, '115200'),
    )

    SERIAL_DEVICE_CHOICES = (
        ('COM1', 'windows COM1'),
        ('COM2', 'windows COM2'),
        ('COM3', 'windows COM3'),
        ('COM4', 'windows COM4'),
        ('COM5', 'windows COM5'),
        ('COM6', 'windows COM6'),
        ('COM7', 'windows COM7'),
        ('COM8', 'windows COM8'),
        ('COM9', 'windows COM9'),
        ('COM10', 'windows COM10'),
        ('COM11', 'windows COM11'),
        ('COM12', 'windows COM12'),
        ('COM13', 'windows COM13'),
        ('COM14', 'windows COM14'),
        ('COM15', 'windows COM15'),
        ('COM16', 'windows COM16'),
        ('COM17', 'windows COM17'),
        ('COM18', 'windows COM18'),
        ('COM19', 'windows COM19'),
        ('/dev/ttyUSB0', 'Linux ttyUSB0'),
        ('/dev/ttyUSB1', 'Linux ttyUSB1'),
        ('/dev/ttyUSB2', 'Linux ttyUSB2'),
        ('/dev/ttyUSB3', 'Linux ttyUSB3'),
        ('/dev/ttyUSB4', 'Linux ttyUSB4'),
        ('/dev/ttyACM0', 'Linux ttyACM0'),
        ('/dev/ttyACM1', 'Linux ttyACM1'),
        ('/dev/ttyACM2', 'Linux ttyACM2'),
        ('/dev/ttyACM3', 'Linux ttyACM3'),
        ('/dev/ttyACM4', 'Linux ttyACM4'),
        ('/dev/rfcomm0', 'Linux rfcomm0'),
        ('/dev/rfcomm1', 'Linux rfcomm1'),
        ('/dev/rfcomm2', 'Linux rfcomm2'),
        ('/dev/tty.HC-05-DevB', 'OSX tty.HC-05-DevB'),
    )

    active = models.BooleanField(ugettext_lazy("Active"),default=False,help_text=ugettext_lazy("Activate this transport for measurements"))
    baudrate = models.PositiveIntegerField(default=9600,null=False,blank=False,choices=SERIAL_BAUDRATE_CHOICES,help_text=ugettext_lazy("Baud rate"))
    device = models.CharField(max_length=30,unique=False,default="/dev/ttyUSB0",null=False,blank=False, choices=SERIAL_DEVICE_CHOICES,help_text=ugettext_lazy("Serial device"))

    board = models.OneToOneField("Board")

    def natural_key(self):
        #print "natural key"
        #print self,self.board.natural_key()
        return (self.board.natural_key(),)

    natural_key.dependencies = ['stations.board']

    class Meta:
        ordering = ['board']
        verbose_name = 'serial transport'
        verbose_name_plural = 'serial transports'

    def __unicode__(self):
        return u'%s' % (self.device)


class TransportBluetoothManager(models.Manager):
    def get_by_natural_key(self, board):
        #print "TransportBluetoothManager: ",board
        return self.get(board=Board.objects.get_by_natural_key(board[0],board[1]))

class TransportBluetooth(models.Model):
    """Bluetooth transport."""

    objects = TransportBluetoothManager()

    active = models.BooleanField(ugettext_lazy("Active"),default=False,help_text=ugettext_lazy("Activate this transport for measurements"))
    name = models.CharField(max_length=80,help_text=ugettext_lazy("bluetooth name"))

    board = models.OneToOneField("Board")

    def natural_key(self):
        #print "natural key"
        #print self,self.board.natural_key()
        return (self.board.natural_key(),)

    natural_key.dependencies = ['stations.board']

    class Meta:
        ordering = ['name']
        verbose_name = 'bluetooth transport'
        verbose_name_plural = 'bluetooth transport'

    def __unicode__(self):
        return u'%s' % (self.name)


class TransportAmqpManager(models.Manager):
    def get_by_natural_key(self, board):
        #print "TransportAmqpManager: ", board
        return self.get(board=Board.objects.get_by_natural_key(board[0],board[1]))

class TransportAmqp(models.Model):
    """amqp transport."""

    objects = TransportAmqpManager()

    active = models.BooleanField(ugettext_lazy("Active"),default=False,help_text=ugettext_lazy("Activate this transport for measurements"))

    amqpserver = models.CharField(max_length=50,default="rmap.cc",null=False,blank=False,help_text=ugettext_lazy("AMQP server"))
    exchange = models.CharField(max_length=50,default="rmap",null=False,blank=False,help_text=ugettext_lazy("AMQP remote exchange name"))
    queue = models.CharField(max_length=50,default="rmap",null=False,blank=False,help_text=ugettext_lazy("AMQP local queue name"))
    amqpuser= models.CharField(max_length=9,default="",null=False,blank=True,help_text=ugettext_lazy("AMQP user"))
    amqppassword= models.CharField(max_length=50,default="",null=False,blank=True,help_text=ugettext_lazy("AMQP password"))

    board = models.OneToOneField("Board")

    def natural_key(self):
        #print "natural key"
        #print self,self.board.natural_key()
        return (self.board.natural_key(),)

    natural_key.dependencies = ['stations.board']

    def __unicode__(self):
        return u'%s' % (self.amqpserver)


class BoardManager(models.Manager):
    def get_by_natural_key(self, slug,stationmetadata):
        #print "BoardManager: ",slug,stationmetadata
        return self.get(slug=slug,stationmetadata=StationMetadata.objects.get_by_natural_key(stationmetadata[0],stationmetadata[1]))

class Board(models.Model):
    """Board model."""

    objects = BoardManager()

    BOARD_CATEGORY_CHOICES = (
        ('base','Raspberry base'),
        ('master', 'Mega2560 master'),
        ('satellite','Microduino core+ satellite'),
        ('gsm','Microduino core+ GSM/GPRS with GPS'),
        ('bluetooth','Microduino core+ with Bluetooth module'),
    )

    name = models.CharField(max_length=255,help_text=ugettext_lazy("station name"))
    active = models.BooleanField(ugettext_lazy("Active"),default=False,help_text=ugettext_lazy("Activate the board for measurements"))
    slug = models.SlugField(unique=False, help_text=ugettext_lazy('Auto-generated from name.'))
    category = models.CharField(max_length=50, blank=False,choices=BOARD_CATEGORY_CHOICES)
    stationmetadata = models.ForeignKey('StationMetadata')

#    def changeform_link(self):
#        if self.id:
#            # Replace "myapp" with the name of the app containing
#            # your Certificate model:
#            changeform_url = urlresolvers.reverse(
#                'admin:station_change', args=(self.id,)
#            )
#            return u'<a href="%s" target="_blank">Details</a>' % changeform_url
#        return u''
#    changeform_link.allow_tags = True
#    changeform_link.short_description = ''   # omit column header

    def natural_key(self):
        #print "natural key"
        #print self,self.slug,self.stationmetadata.natural_key()
        return (self.slug,self.stationmetadata.natural_key())

    natural_key.dependencies = ['stations.stationmetadata']

    class Meta:
        ordering = ['slug']
        verbose_name = 'hardware board'
        verbose_name_plural = 'hardware boards'
        unique_together = (('slug', 'stationmetadata'),)

    def __unicode__(self):
        return u'%s' % (self.slug)

class StationConstantDataManager(models.Manager):
    def get_by_natural_key(self, btable,stationmetadata):
        #print "StationConstantDataManager: ", stationmetadata
        return self.get( btable=btable, stationmetadata=StationMetadata.objects.get_by_natural_key(stationmetadata[0],stationmetadata[1]))

class StationConstantData(models.Model):
    """Station constant metadata."""

    objects = StationConstantDataManager()

    BTABLE_CHOICES = (
        ("B01019","LONG STATION OR SITE NAME                                        (CCITTIA5)"),
        ("B02001","TYPE OF STATION                                                  (CODE TABLE 2001)"),
        ("B02002","TYPE OF INSTRUMENTATION FOR WIND MEASUREMENT                     (FLAG TABLE 2002)"),
        ("B02003","TYPE OF MEASURING EQUIPMENT USED                                 (CODE TABLE 2003)"),
        ("B02004","TYPE OF INSTRUMENTATION FOR EVAPORATION MEASUREMENT OR TYPE OF C (CODE TABLE 2004)"),
        ("B02005","PRECISION OF TEMPERATURE OBSERVATION                             (K*100)"),
        ("B02038","METHOD OF WATER TEMPERATURE AND/OR SALINITY MEASUREMENT          (CODE TABLE 2038)"),
        ("B02039","METHOD OF WET-BULB TEMPERATURE MEASUREMENT                       (CODE TABLE 2039)"),
        ("B07030","HEIGHT OF STATION GROUND ABOVE MEAN SEA LEVEL (SEE NOTE 3)       (m*10)"),
        ("B07031","HEIGHT OF BAROMETER ABOVE MEAN SEA LEVEL (SEE NOTE 4)            (m*10)"),
    )

    active = models.BooleanField(ugettext_lazy("Active"),default=True,help_text=ugettext_lazy("Activate this metadata"))
    btable = models.CharField(max_length=6,unique=False,blank=False,choices=BTABLE_CHOICES,help_text=ugettext_lazy("A code to define the metadata. See rmap RFC"))
    value=models.CharField(max_length=32,null=False,blank=False,help_text=ugettext_lazy("value for associated B table"))
    stationmetadata = models.ForeignKey('StationMetadata')

    def natural_key(self):
        #print "natural key"
        #print self,self.btable, self.stationmetadata.natural_key()
        return (self.btable, self.stationmetadata.natural_key())

    natural_key.dependencies = ['stations.stationmetadata']

    class Meta:
        ordering = ['btable']
        verbose_name = 'Station constant metadata'
        verbose_name_plural = 'Station constant metadata'
        unique_together = (('btable', 'stationmetadata'),)

    def __unicode__(self):
        return u'%s' % (self.btable)

class StationMetadataManager(models.Manager):
    def get_by_natural_key(self, slug, ident):
        #print "StationMetadataManager: ", slug,ident
        return self.get(slug=slug, ident=User.objects.get_by_natural_key(ident[0]))

class StationMetadata(models.Model):
    """Station Metadata."""

    objects = StationMetadataManager()

    STATION_CATEGORY_CHOICES = (
        ('good','Beautifull & Good'),
        ('bad', 'Bad & Wrong'),
        ('test','Test & Bugs'),
        ('unknown','Unknown & Missing'),
    )


    name = models.CharField(max_length=255,help_text=ugettext_lazy("station name"))
    active = models.BooleanField(ugettext_lazy("Active"),default=True,help_text=ugettext_lazy("Activate the station for measurements"))
    slug = models.SlugField(unique=False, help_text=ugettext_lazy('Auto-generated from name.'))

    ident = models.ForeignKey(User)
    #ident = models.ForeignKey(User, limit_choices_to={'is_staff': True})

#    ident = models.CharField(max_length=9,unique=False,null=False,blank=True, help_text=ugettext_lazy("station identifier (should be equal to your username)"))

    lat = models.FloatField(ugettext_lazy("Latitude"),default=None,null=False,blank=False, help_text=ugettext_lazy('Precise Latitude of the station'))
    lon = models.FloatField(ugettext_lazy("Longitude"),default=None,null=False,blank=False, help_text=ugettext_lazy('Precise Longitude of the station'))

    network = models.CharField(max_length=50,default="rmap",unique=False,null=False,blank=False, help_text=ugettext_lazy("station network"))

    mqttrootpath = models.CharField(max_length=100,default="rmap",null=False,blank=False,help_text=ugettext_lazy("root mqtt path for publish"))
    mqttmaintpath = models.CharField(max_length=100,default="rmap",null=False,blank=False,help_text=ugettext_lazy("maint mqtt path for publish"))
    category = models.CharField(max_length=50, choices=STATION_CATEGORY_CHOICES,help_text=ugettext_lazy("Category of the station"))

    def lon_lat(self):
        return "%d_%d" % (nint(self.lon*100000),nint(self.lat*100000))

    def natural_key(self):
        #print "StationMetadata natural_key"
        #print self,self.slug, self.ident.natural_key()
        return (self.slug, self.ident.natural_key())

    natural_key.dependencies = ['auth.user']

    class Meta:
        ordering = ['slug']
        verbose_name = 'station'
        verbose_name_plural = 'stations'
        unique_together = (('slug', 'ident'),)


    def __unicode__(self):
        return u'%s-%s' % (self.slug,self.ident)


from django.contrib.auth.models import User


class UserProfileManager(models.Manager):
    def get_by_natural_key(self, user):
        #print "UserProfileManager: ",user
        return self.get(user=User.objects.get_by_natural_key(user[0]))

class UserProfile(models.Model):

    objects = UserProfileManager()

    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    accepted_license = models.BooleanField(ugettext_lazy("I accept ODBL license"),default=False,null=False,blank=False,help_text=ugettext_lazy("You need to accept ODBL license to provide your data"))
    certification = models.CharField(max_length=20, default="ARPA-ER")

    def natural_key(self):
        #print "UserProfile natural_key"
        #print self,self.user.natural_key()
        return (self.user.natural_key(),)

    natural_key.dependencies = ['auth.user']

from django.db.models.signals import post_save

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
