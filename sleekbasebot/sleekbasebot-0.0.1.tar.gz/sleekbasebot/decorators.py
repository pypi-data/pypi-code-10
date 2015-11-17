__author__ = 'meatpuppet'


import logging

def admin_only(reply_string='admins only!'):
    '''
    decorates functions to be only executed by admins.
    replies reply_string if called by none-admin, or nothing if reply_string is empty

    :param reply_string:
    :return:
    '''

    def dec(func):
        def wrap(bot, msg):
            admins = bot.settings['admins']
            sender=msg.get('from').bare
            if sender in admins:
                func(bot, msg)
            else:
                logging.debug('admin command %s called by non-admin %s' % (msg['body'].split()[0], sender))
                if reply_string:
                    msg.reply(reply_string).send()
        return wrap
    return dec

def arguments(*args, **kwargs):
    '''
    parses the message for arguments

    :return:
    '''
    def dec(func):
        def wrap(bot, msg):
            message_split=msg['body'].split()
            print(len(message_split)-1)
            if len(message_split)-1 >= kwargs.get('min', 0):

                # combine args and msg_split
                func_kwargs = {}
                func_kwargs['sender'] = msg['from']
                func_kwargs['bot'] = bot
                for arg in args:
                    try:
                        func_kwargs[arg] = message_split.pop(1)
                        #print('got arg %s: %s' % (arg,func_kwargs[arg] ))
                    except:
                        func_kwargs[arg] = None
                logging.debug('calling bot func with kwargs: %s' % func_kwargs)
                func(msg, **func_kwargs)
                return

            if kwargs['usage']:
                logging.debug('sending usage (got %s -> %s arguments)' % (message_split, len(message_split)-1))
                msg.reply('usage: ' + kwargs['usage']).send()
        return wrap
    return dec