#!/usr/bin/env python
# encoding: utf-8
"""
Copyright (c) 2014 Cross Technology AB

"""
from __future__ import unicode_literals
import urllib
import datetime
from .exc import *

import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape as xml_escape


class SMSTeknikClient(object):
    """
    Client for the SMS Teknik Gateway API.

    Parameters:
        id (str): Company name
        user (str): Account username
        password (str): Account password

    Other Parameters:
        deliverystatusaddress (str): Email or URL for report
        deliverystatustype (str): Delivery report method

            'off'  - No delivery status (Default)

            'email' - Email

            'get' - HTTP GET

            'post' - HTTP POST

            'xml' - HTTP XML

        smssender (str): Sender shown to recipients
        multisms (bool): Allow message splitting (Supported on most modern phones)
        url (str): API URL, (Default: https://www.smsteknik.se/Member/SMSConnectDirect/SendSMSv3.asp )

    Example:
        >>> client = SMSTeknikClient(id=..., user=..., password=..., ...)
        >>> client.send(['+4673XXXXXXX', '+46707XXXXXX'], 'Hello Wörld!')
        [
            { 'number': '+4673XXXXXXX', 'SMSID': 01234 },
            { 'number': '+46707XXXXXX', 'SMSID': 49312 }
        ]
    
    """

    _errors = {
            'Access denied': AccessDenied,
            'No SMS left':  NoSMSLeft,
            'Parse error':  ParseError,
            'The required XML-tag <udmessage> is missing': ParseError,
            # Yes, the typo is actually in the API
            "Message could't be empty": EmptyMessage,
            'Invalid phonenumber':      InvalidPhonenumber,
            'Number is blocked':        BlockedNumber
            }


    _deliverystatustype_name = {
            None: 0,
            'off': 0,
            'email': 1,
            'get': 2,
            'post': 3,
            'xml': 4}

    # Consult the Manual for specifications on the XML
    _xml_template = """<?xml version="1.0" encoding="utf-8" ?>
        <sms-teknik>
            <operationtype>0</operationtype>
            <flash>0</flash>
            <multisms>{multisms}</multisms>
            <maxmultisms>0</maxmultisms>
            <compresstext>0</compresstext>
            <udmessage><![CDATA[{message}]]></udmessage>
            <smssender>{smssender}</smssender>
            <deliverystatustype>{deliverystatustype}</deliverystatustype>
            <deliverystatusaddress>{deliverystatusaddress}</deliverystatusaddress>
            <usereplynumber>{usereplynumber}</usereplynumber>
            <usereplyforwardtype>{usereplyforwardtype}</usereplyforwardtype>
            <usereplyforwardurl>{usereplyforwardurl}</usereplyforwardurl>
            <usereplycustomid></usereplycustomid>
            <usee164>0</usee164>
            <items>        
                {items}
            </items>        
        </sms-teknik>"""

    _recipients_template = """
        <recipient>
            <orgaddress>{recipient}</orgaddress> 
        </recipient>
    """

    # Delivery status request template, currently only one smsid at a time
    _delivery_status_request_template = """<?xml version="1.0" ?>
        <sms-teknik>
            <smsid>{smsid}</smsid>
        </sms-teknik>
    """

    _default_options = {
        'id': None,
        'user': None,
        'password': None,
        'deliverystatustype': 0,
        'deliverystatusaddress': '',
        'usereplynumber': 0,
        'usereplyforwardtype': 0,
        'usereplyforwardurl': '',
        'smssender': '',
        'multisms': 1,
        'url': 'https://www.smsteknik.se/Member/SMSConnectDirect',
        'send_path': 'SendSMSv3.asp',
        'status_path': 'GetStatusv2.asp'
    }

    def __init__(self, **kwargs):
        """SMSTeknik interface
        """
        self.options = {opt: kwargs.get(opt, default)
            for (opt, default) in self._default_options.iteritems()}

        self.options['deliverystatustype'] = self._deliverystatustype_name.get(
                self.options['deliverystatustype'],
                self.options['deliverystatustype'])

        intopts = ['deliverystatustype', 'usereplynumber', 'usereplyforwardtype', 'multisms']
        for key in intopts:
            self.options[key] = int(self.options[key])

        required = ['id', 'user', 'password']
        for key in required:
            if self.options[key] is None:
                raise ValueError("Missing argument: {}".format(key))

    def _recipient_entry(self, recipient):
        '''
        Create xml for recipient

        Parameters:
            recipient (string): Number
        '''
        return self._recipients_template.format(
                recipient=xml_escape(recipient)
                )

    def send(self, recipients, message):
        """
        Send an SMS

        Raises `SMSTeknikError` if the API gives less responses than there
        are recipients.

        Parameters:
            recipients (list): Phone numbers
            message (str): Message to send

        Returns:
            list: dicts with number, SMSID and possibly error


        Example:

            >>> client.send(['123 456', 'not a number'], 'hi.')
            [
                {'number': '123 456', 'SMSID': 0000},
                {'number': 'not a number', 'SMSID': None, 'error': InvalidPhonenumber('Invalid phonenumber #not a number#')}
             ]

        """
        if not (self.options['multisms'] == 1) and len(message) > 160:
            raise ValueError("Max SMS size is 160 characters")

        items = [self._recipient_entry(r) for r in recipients]

        xml = self._xml_template.format(
            message = message,
            items   = '\n'.join(items),
            **self.options
        )

        # Create the URL used for POSTing the XML
        url = "{url}/{send_path}?id={quoted_id}&user={user}&pass={password}".format(
                quoted_id=urllib.quote_plus(self.options['id']),
                **self.options
        )

        # Call the Gateway API with the XML as POST-data
        f = urllib.urlopen(url, xml.encode('utf-8'))
        raw_results = f.read().split(';')

        if len(raw_results) != len(recipients):
            # Not same number of results as recipients
            # wont be able to parse the result properly
            error = self._get_error(raw_results[0])
            if error is None:
                raise SMSTeknikError(raw_results)
            else:
                raise error

        results = self._parse_result(raw_results, recipients)

        return results

    def delivery_status(self, sms_id):
        """ Get the delivery status of a previously sent SMS.

        Parameters:
            sms_id (int): SMSID returned from a call to send

        Returns:
            dict: A dict representing the response returned from SMS Teknik. The dict
            will have the following keys and values:

                {
                    "smsid": 1234,
                    "state": "DELIVRD",
                    "donedate": datetime,
                    "customid": "String with something",
                    "smsparts": 1
                }

        """

        xml = self._delivery_status_request_template.format(smsid=sms_id)

        url = "{url}/{status_path}?id={quoted_id}&user={user}&pass={password}".format(
                quoted_id=urllib.quote_plus(self.options['id']),
                **self.options
        )

        # Call the Gateway API with the XML as POST-data
        f = urllib.urlopen(url, xml.encode('utf-8'))
        raw_results = f.readlines()

        result = None
        if len(raw_results) >= 1:
            result = self._parse_status_response(raw_results[0])

        return result

    def _parse_status_response(self, xml):
        """ Parse the specified xml string and return the contents as a dictionary. If
        the specified xml string cannot be parsed, or if an error occurs None will
        be returned

        Parameters:
            xml (str): A XML formatted string containing a response from SMS Tekniks
                delivery status endpoint.
        Returns:
            dict: A dictionary representing the response;

                {
                    "smsid": 1234,
                    "state": "DELIVRD",
                    "donedate": datetime,
                    "customid": "String with something",
                    "smsparts": 1
                }

            Description of the values can be found in SMS Tekniks documentation
        """

        def get_node_value(elm, path, default=None, type=str, dt_format='%Y-%m-%d %H:%M:%S'):
            e = elm.find(path)
            if e is not None:
                if type == datetime.datetime:
                    if e.text is not None and e.text != '0':
                        return datetime.datetime.strptime(e.text, dt_format)
                    else:
                        return None
                return type(e.text)

            return default

        result = None
        try:
            root = ET.fromstring(xml)
            result = {
                'smsid': get_node_value(root, './item/smsid', type=int),
                'state': get_node_value(root, './item/state'),
                'donedate': get_node_value(root, './item/donedate', type=datetime.datetime),
                'customid': get_node_value(root, './item/customid'),
                'smsparts': get_node_value(root, './item/smsparts', type=int)
            }
        except Exception as e:
            result = None

        return result

    def _parse_result(self, result, recipients):
        """
        Parse the semi-colon separated status responses

        Returns a list of dicts with 'number' and 'SMSID' for each recipient
        If the send failed the 'SMSID' will be None and there will be an
        'error' item with the corresponding exception as defined in the Gateway API
        in the call to _get_error()

        Note that the exceptions are not raised.
        """
        parsed = []
        for number, entry in zip(recipients, result):
            error = self._get_error(entry)
            if error is None:
                parsed.append({'number': number, 'SMSID': entry})
            else:
                parsed.append({'number': number, 'SMSID': None, 'error': error})
        return parsed

    def _get_error(self, err_code):
        """
        Returns exception corresponding to error code, or None
        if it was a normal condition (just numbers)
        """
        if err_code.isdigit():
            # Normal condition, just an SMSID
            return None

        err_msg = err_code.split(':')[-1]
        for err_start, exc in self._errors.iteritems():
            if err_msg.startswith(err_start):
                return exc(err_msg)

        # Unknown error, return the generic error
        return SMSTeknikError(err_msg)
