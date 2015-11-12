#    mailplate - send muli-language multi-transport template-driven email
#    Copyright (c) 2015 Avner Herskovits
#
#    MIT License
#
#    Permission  is  hereby granted, free of charge, to any person  obtaining  a
#    copy of this  software and associated documentation files (the "Software"),
#    to deal in the Software  without  restriction, including without limitation
#    the rights to use, copy, modify, merge,  publish,  distribute,  sublicense,
#    and/or  sell  copies of  the  Software,  and to permit persons to whom  the
#    Software is furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this  permission notice shall be included in
#    all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT  WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE  WARRANTIES  OF  MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR  ANY  CLAIM,  DAMAGES  OR  OTHER
#    LIABILITY, WHETHER IN AN  ACTION  OF  CONTRACT,  TORT OR OTHERWISE, ARISING
#    FROM,  OUT  OF  OR  IN  CONNECTION WITH THE SOFTWARE OR THE  USE  OR  OTHER
#    DEALINGS IN THE SOFTWARE.
#
from email.mime.multipart   import MIMEMultipart
from email.mime.text        import MIMEText
from gettext                import translation
from importlib. machinery   import SourceFileLoader
from os                     import listdir
from os. path               import dirname, isdir, isfile, join
from urllib. parse          import urlparse

class Mailplate:
    def __init__( self, mailer, credentials, send_from, locale_dir, gettext_domain, default_lang, messages ):
        self. creds     = credentials
        self. from_     = send_from
        self. def_lang  = default_lang
        self. msgs      = { msg: {} for msg in messages }
        for lang in [ fn for fn in listdir( locale_dir ) if isdir( locale_dir + '/' + fn )]:
            xlator = translation( gettext_domain, locale_dir, [ lang ])
            for msg in messages:
                tmp = [ xlator. gettext( msg + ':subject' ), xlator. gettext( msg + ':text' ), xlator. gettext( msg + ':html' )]
                if lang == default_lang and ( None == tmp[ 0 ] or ( None == tmp[ 1 ] and None == tmp[ 2 ])):
                    raise ValueError( 'Default languange must have a subject and body defined for each message' )
                elif [ None, None, None ] != tmp:
                    self. msgs[ msg ][ lang ] = tmp
        self. mailer = urlparse( mailer )
        if None == self. mailer. scheme:
            raise ValueError( 'The mailer must have a scheme, e.g. smtps://' )
        driver = join( dirname( __file__ ), 'driver', self. mailer. scheme + '.py' )
        if not isfile( driver ):
            raise ValueError( 'Missing transport driver for ' + self. mailer. scheme + '://' )
        self. driver = SourceFileLoader( 'mailplate_' + self. mailer. scheme, driver ). load_module()
        
    def send( self, to, msg, lang, args = {} ):
        _args = args
        _args[ 'to' ] = to
        _msg = self. msgs[ msg ][ lang ] if lang in self. msgs[ msg ] else [ None, None, None ]
        if None in _msg:
            if '_' in lang:
                _lang, _rest = lang. split( '_', 1 )
                if _lang in self. msgs[ msg ]:
                    for i in range( 0, 3 ):
                        if None == _msg[ i ]:
                            _msg[ i ] = self. msgs[ msg ][ _lang ][ i ]
            if None in _msg:
                for i in range( 0, 3 ):
                    if None == _msg[ i ]:
                        _msg[ i ] = self. msgs[ msg ][ self. def_lang ][ i ]
        for i in range( 0, 3 ):
            if None != _msg[ i ]:
                _msg[ i ] = _msg[ i ]. format( **_args )
        mime = MIMEMultipart( 'alternative' )
        mime[ 'Subject' ]   = _msg[ 0 ]
        mime[ 'From' ]      = self. from_
        mime[ 'To' ]        = to
        if None != _msg[ 1 ]: mime. attach( MIMEText( _msg[ 1 ], 'text' ))
        if None != _msg[ 2 ]: mime. attach( MIMEText( _msg[ 2 ], 'html' ))
        self. driver. send( self. mailer, self. creds, mime )

#
# Sample usage
#
if '__main__' == __name__:
    pass    # Comment this line when running the samples below
#
# Uncomment ONE of the following initializers and fill-in the credentials:
#
    #mailplate = Mailplate( 'smtp://localhost:2500/', None, 'foo@example.com', 'example', 'mailplate', 'en_US', [ 'message-1', 'message-2' ])
    #mailplate = Mailplate( 'smtps://smtp.gmail.com:587/', ( my-username, my-password ), from-address, 'example', 'mailplate', 'en_US', [ 'message-1', 'message-2' ])
    #mailplate = Mailplate( 'ses://', ( access-key-id, secret-access-key, region ), from-address, 'example', 'mailplate', 'en_US', [ 'message-1', 'message-2' ])
    #mailplate = Mailplate( 'mailgun://', ( sender-domain, api-key ), from-address, 'example', 'mailplate', 'en_US', [ 'message-1', 'message-2' ])
#
# Now send as many messages:
#
    #mailplate. send( 'test-address1@example.com', 'message-1', 'en_GB', args = { 'param': 123 })
    #mailplate. send( 'test-address2@example.com', 'message-1', 'en_CA', args = { 'param': 123 })
    #mailplate. send( 'test-address3@example.com', 'message-1', 'de',    args = { 'param': 123 })



