# -*- encoding: utf-8 -*-

from .database import db
from .device import Device
from .user import User
from .vpn import Vpn

session = db.session
