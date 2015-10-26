# Copyright (c) 2010 Mitch Garnaat http://garnaat.org/
# Copyright (c) 2011 Harry Marr http://hmarr.com/
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from boto.connection import AWSAuthConnection
from boto.exception import BotoServerError
from boto.regioninfo import RegionInfo
import boto
import boto.jsonresponse

import urllib
import base64
from boto.ses import exceptions as ses_exceptions


class SESConnection(AWSAuthConnection):

    ResponseError = BotoServerError
    DefaultRegionName = 'us-east-1'
    DefaultRegionEndpoint = 'email.us-east-1.amazonaws.com'
    APIVersion = '2010-12-01'

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None,
                 is_secure=True, port=None, proxy=None, proxy_port=None,
                 proxy_user=None, proxy_pass=None, debug=0,
                 https_connection_factory=None, region=None, path='/'):
        if not region:
            region = RegionInfo(self, self.DefaultRegionName,
                                self.DefaultRegionEndpoint)
        self.region = region
        AWSAuthConnection.__init__(self, self.region.endpoint,
                                   aws_access_key_id, aws_secret_access_key,
                                   is_secure, port, proxy, proxy_port,
                                   proxy_user, proxy_pass, debug,
                                   https_connection_factory, path)

    def _required_auth_capability(self):
        return ['ses']

    def _build_list_params(self, params, items, label):
        """Add an AWS API-compatible parameter list to a dictionary.

        :type params: dict
        :param params: The parameter dictionary

        :type items: list
        :param items: Items to be included in the list

        :type label: string
        :param label: The parameter list's name
        """
        if isinstance(items, basestring):
            items = [items]
        for i in range(1, len(items) + 1):
            params['%s.%d' % (label, i)] = items[i - 1]

    def _make_request(self, action, params=None):
        """Make a call to the SES API.

        :type action: string
        :param action: The API method to use (e.g. SendRawEmail)

        :type params: dict
        :param params: Parameters that will be sent as POST data with the API
            call.
        """
        ct = 'application/x-www-form-urlencoded; charset=UTF-8'
        headers = {'Content-Type': ct}
        params = params or {}
        params['Action'] = action

        for k, v in params.items():
            if isinstance(v, unicode):  # UTF-8 encode only if it's Unicode
                params[k] = v.encode('utf-8')

        response = super(SESConnection, self).make_request(
            'POST',
            '/',
            headers=headers,
            data=urllib.urlencode(params)
        )
        body = response.read()
        if response.status == 200:
            list_markers = ('VerifiedEmailAddresses', 'SendDataPoints')
            e = boto.jsonresponse.Element(list_marker=list_markers)
            h = boto.jsonresponse.XmlHandler(e, None)
            h.parse(body)
            return e
        else:
            # HTTP codes other than 200 are considered errors. Go through
            # some error handling to determine which exception gets raised,
            self._handle_error(response, body)

    def _handle_error(self, response, body):
        """
        Handle raising the correct exception, depending on the error. Many
        errors share the same HTTP response code, meaning we have to get really
        kludgey and do string searches to figure out what went wrong.
        """
        boto.log.error('%s %s' % (response.status, response.reason))
        boto.log.error('%s' % body)

        if "Address blacklisted." in body:
            # Delivery failures happened frequently enough with the recipient's
            # email address for Amazon to blacklist it. After a day or three,
            # they'll be automatically removed, and delivery can be attempted
            # again (if you write the code to do so in your application).
            ExceptionToRaise = ses_exceptions.SESAddressBlacklistedError
            exc_reason = "Address blacklisted."
        elif "Email address is not verified." in body:
            # This error happens when the "Reply-To" value passed to
            # send_email() hasn't been verified yet.
            ExceptionToRaise = ses_exceptions.SESAddressNotVerifiedError
            exc_reason = "Email address is not verified."
        elif "Daily message quota exceeded." in body:
            # Encountered when your account exceeds the maximum total number
            # of emails per 24 hours.
            ExceptionToRaise = ses_exceptions.SESDailyQuotaExceededError
            exc_reason = "Daily message quota exceeded."
        elif "Maximum sending rate exceeded." in body:
            # Your account has sent above its allowed requests a second rate.
            ExceptionToRaise = ses_exceptions.SESMaxSendingRateExceededError
            exc_reason = "Maximum sending rate exceeded."
        elif "Domain ends with dot." in body:
            # Recipient address ends with a dot/period. This is invalid.
            ExceptionToRaise = ses_exceptions.SESDomainEndsWithDotError
            exc_reason = "Domain ends with dot."
        else:
            # This is either a common AWS error, or one that we don't devote
            # its own exception to.
            ExceptionToRaise = self.ResponseError
            exc_reason = response.reason

        raise ExceptionToRaise(response.status, exc_reason, body)

    def send_email(self, source, subject, body, to_addresses, cc_addresses=None,
                   bcc_addresses=None, format='text', reply_addresses=None,
                   return_path=None, text_body=None, html_body=None):
        """Composes an email message based on input data, and then immediately
        queues the message for sending.

        :type source: string
        :param source: The sender's email address.

        :type subject: string
        :param subject: The subject of the message: A short summary of the
                        content, which will appear in the recipient's inbox.

        :type body: string
        :param body: The message body.

        :type to_addresses: list of strings or string
        :param to_addresses: The To: field(s) of the message.

        :type cc_addresses: list of strings or string
        :param cc_addresses: The CC: field(s) of the message.

        :type bcc_addresses: list of strings or string
        :param bcc_addresses: The BCC: field(s) of the message.

        :type format: string
        :param format: The format of the message's body, must be either "text"
                       or "html".

        :type reply_addresses: list of strings or string
        :param reply_addresses: The reply-to email address(es) for the
                                message. If the recipient replies to the
                                message, each reply-to address will
                                receive the reply.

        :type return_path: string
        :param return_path: The email address to which bounce notifications are
                            to be forwarded. If the message cannot be delivered
                            to the recipient, then an error message will be
                            returned from the recipient's ISP; this message will
                            then be forwarded to the email address specified by
                            the ReturnPath parameter.

        :type text_body: string
        :param text_body: The text body to send with this email.

        :type html_body: string
        :param html_body: The html body to send with this email.

        """
        format = format.lower().strip()
        if body is not None:
            if format == "text":
                if text_body is not None:
                    raise Warning("You've passed in both a body and a text_body; please choose one or the other.")
                text_body = body
            else:
                if html_body is not None:
                    raise Warning("You've passed in both a body and an html_body; please choose one or the other.")
                html_body = body

        params = {
            'Source': source,
            'Message.Subject.Data': subject,
        }

        if return_path:
            params['ReturnPath'] = return_path

        if html_body is not None:
            params['Message.Body.Html.Data'] = html_body
        if text_body is not None:
            params['Message.Body.Text.Data'] = text_body

        if(format not in ("text","html")):
            raise ValueError("'format' argument must be 'text' or 'html'")

        if(not (html_body or text_body)):
            raise ValueError("No text or html body found for mail")

        self._build_list_params(params, to_addresses,
                               'Destination.ToAddresses.member')
        if cc_addresses:
            self._build_list_params(params, cc_addresses,
                                   'Destination.CcAddresses.member')

        if bcc_addresses:
            self._build_list_params(params, bcc_addresses,
                                   'Destination.BccAddresses.member')

        if reply_addresses:
            self._build_list_params(params, reply_addresses,
                                   'ReplyToAddresses.member')

        return self._make_request('SendEmail', params)

    def send_raw_email(self, raw_message, source=None, destinations=None):
        """Sends an email message, with header and content specified by the
        client. The SendRawEmail action is useful for sending multipart MIME
        emails, with attachments or inline content. The raw text of the message
        must comply with Internet email standards; otherwise, the message
        cannot be sent.

        :type source: string
        :param source: The sender's email address. Amazon's docs say:

          If you specify the Source parameter, then bounce notifications and
          complaints will be sent to this email address. This takes precedence
          over any Return-Path header that you might include in the raw text of
          the message.

        :type raw_message: string
        :param raw_message: The raw text of the message. The client is
          responsible for ensuring the following:

          - Message must contain a header and a body, separated by a blank line.
          - All required header fields must be present.
          - Each part of a multipart MIME message must be formatted properly.
          - MIME content types must be among those supported by Amazon SES.
            Refer to the Amazon SES Developer Guide for more details.
          - Content must be base64-encoded, if MIME requires it.

        :type destinations: list of strings or string
        :param destinations: A list of destinations for the message.

        """
        params = {
            'RawMessage.Data': base64.b64encode(raw_message),
        }

        if source:
            params['Source'] = source

        if destinations:
            self._build_list_params(params, destinations,
                                   'Destinations.member')

        return self._make_request('SendRawEmail', params)

    def list_verified_email_addresses(self):
        """Fetch a list of the email addresses that have been verified.

        :rtype: dict
        :returns: A ListVerifiedEmailAddressesResponse structure. Note that
                  keys must be unicode strings.
        """
        return self._make_request('ListVerifiedEmailAddresses')

    def get_send_quota(self):
        """Fetches the user's current activity limits.

        :rtype: dict
        :returns: A GetSendQuotaResponse structure. Note that keys must be
                  unicode strings.
        """
        return self._make_request('GetSendQuota')

    def get_send_statistics(self):
        """Fetches the user's sending statistics. The result is a list of data
        points, representing the last two weeks of sending activity.

        Each data point in the list contains statistics for a 15-minute
        interval.

        :rtype: dict
        :returns: A GetSendStatisticsResponse structure. Note that keys must be
                  unicode strings.
        """
        return self._make_request('GetSendStatistics')

    def delete_verified_email_address(self, email_address):
        """Deletes the specified email address from the list of verified
        addresses.

        :type email_adddress: string
        :param email_address: The email address to be removed from the list of
                              verified addreses.

        :rtype: dict
        :returns: A DeleteVerifiedEmailAddressResponse structure. Note that
                  keys must be unicode strings.
        """
        return self._make_request('DeleteVerifiedEmailAddress', {
            'EmailAddress': email_address,
        })

    def verify_email_address(self, email_address):
        """Verifies an email address. This action causes a confirmation email
        message to be sent to the specified address.

        :type email_adddress: string
        :param email_address: The email address to be verified.

        :rtype: dict
        :returns: A VerifyEmailAddressResponse structure. Note that keys must
                  be unicode strings.
        """
        return self._make_request('VerifyEmailAddress', {
            'EmailAddress': email_address,
        })
