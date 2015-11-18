__author__ = 'meatpuppet'

from sleekbasebot.decorators import arguments

@arguments('topic', min=0, usage='!help [command]')
def command_help(msg, **kwargs):
    '''

    :return:
    '''
    if kwargs['topic']:
        topic = kwargs['bot'].commands.get(kwargs['topic'], False)
        if not topic:
            topic = kwargs['bot'].commands.get('!' + kwargs['topic'], False)
        #try:
        msg['body']=''
        topic(kwargs['bot'], msg)
        #except:
            #msg.reply('i have no help about that').send()
    else:
        msg.reply('commands: %s\n(try !help <command>)' % ', '.join(kwargs['bot'].commands.keys())).send()