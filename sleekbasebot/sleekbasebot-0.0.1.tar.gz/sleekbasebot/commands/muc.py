__author__ = 'meatpuppet'

from sleekbasebot.decorators import arguments

@arguments('roomname', 'password', min=1, usage='!join <room>')
def command_join_room(msg, **kwargs):
    room = kwargs['roomname']
    password = kwargs.get('password', None)
    #logging.info('joining %s' % room)
    kwargs['bot'].plugin['xep_0045'].joinMUC(room,
                                kwargs['bot'].jid.split('@')[0],
                                # If a room password is needed, use:
                                password=password,
                                wait=True)
