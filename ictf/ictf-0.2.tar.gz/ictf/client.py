#
# The iCTF game client.
#
# Written by subwire and the iCTF team, 2015
#
# Because websites are so 1995.
#
import json
import requests
import base64
import random

DEFAULT_GAME_INTERFACE = "https://api.ictf2015.net/"

class iCTF(object):
    """
    The iCTF client!

    If you're just getting started, you probably want to register a team.
    You can access the interactive registration wizard like this:
    >>> from ictf import iCTF()
    >>> i = iCTF()
    >>> i.register_wizard()

    Afterward, your password will be emailed to the email address you specified.
    With that, you can now login:
    >>> t = i.login('team@acme.edu', 'asdfSLKDFSJL')

    Check out the other methods in this class for all kinds of useful functions.

    Have fun!
    - The iCTF Team
    """

    def __init__(self, game_interface=DEFAULT_GAME_INTERFACE):
        self.game_url = game_interface
        self._token = None

    def _post_json(self,endpoint,j):
        # EG says: Why can't Ubuntu stock a recent version of Requests??? Ugh.
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        resp = requests.post(self.game_url + endpoint, data=json.dumps(j), headers=headers)
        try:
            js = json.loads(resp.content)
            return js, resp.status_code
        except:
            return "", resp.status_code
        

    def _get_json(self, endpoint):
        resp = requests.get(self.game_url + endpoint)
        try:
            js = json.loads(resp.content)
            return js, resp.status_code
        except:
            return "", resp.status_code

    # Flag parameters, borrowed from the gamebot
    FLAG_ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    FLAG_LENGTH = 13
    FLAG_PREFIX = "FLG"
    FLAG_SUFFIX = ""

    @staticmethod
    def generate_flag():
        """Generates flags, in the same manner as the game bot.
           This is useful for creating realistic-looking benign traffic for services.
    
        :return: Flag following the predefined flag format.
        """
        flag = "".join(random.choice(iCTF.FLAG_ALPHABET)
                   for _ in range(iCTF.FLAG_LENGTH))
        return "{0}{1}{2}".format(iCTF.FLAG_PREFIX, flag, iCTF.FLAG_SUFFIX)


    def get_metadata_labels(self):
        resp, code = self._get_json("api/metadata")
        if code == 200:
            return resp
        if resp and resp.has_key('message'):
            raise RuntimeError(resp['message'])
        else:
            raise RuntimeError("An unknown error occurred contacting the iCTF server!")

    def register_team(self, name, email, country, logo, alt_email="", metadata={}):
        """
        Register a team
        :param name: The team name
        :param email: The team's primary POC email
        :param country: The team's 2-letter ISO country code
        :param alt_email: The team's alternate email address
        :param logo: File path to the team's PNG logo, 256x256
        :param metadata: Dictionary of metadata responses.  See "get_metadata_labels"
        :return: A CAPTCHA! (Yes! Really!)
        """
        try:
            with open(logo,'rb') as f:
                logo_data = base64.b64encode(f.read())
        except:
            raise RuntimeError("Could not open logo file!")

        args = {'name':name,
                'team_email': team_email,
                'country': country,
                'url': alt_email,
                'logo': logo_data,
                'metadata': metadata}

        resp, code = self._post_json('api/team', args)
        if code == 200:
            return resp['captcha']
        raise RuntimeError(resp['message'])

    def verify(self, response):
        """
        Verify a captcha response, and sign up your team!
        This will send an email to your POCs with your team password!
        :param response: The CAPTCHA response
        :return: None
        """
        args = {'response': response.strip()}
        ret, code = self._post_json('api/team/verify', args)
        if code != 200:
            print ret
            return False
        return True

    def register_wizard(self):
        """
        The interactive iCTF setup wizard! OMFG!!
        Walks you through signup, including entering metadata,
        CAPTCHA, etc
        :return: none
        """
        labels_ret = self.get_metadata_labels()
        if not labels_ret:
            print "Error connecting to iCTF server"
            return
        labels = labels_ret['labels']
        print "Hi! Welcome to iCTF! "
        args = {}
        args['name'] = raw_input("Please enter your team name: ")
        args['team_email'] = raw_input("Please enter your team's primary POC email.  "
                                  "We will send the game password here: ")
        args['url'] = raw_input("[optional] Please enter a URL for your team (e.g., team's web page): ")
        while True:
            try:
                logo_fp = raw_input("[optional] Please enter the local file path to your team's logo (a 256x256 PNG): ")
                if not logo_fp.strip():
                    print "OK fine, going without a logo."
                    break
                with open(logo_fp,'rb') as f:
                    args['logo'] = base64.b64encode(f.read())
                    break
            except:
                print "Couldn't open logo! Try again."

        args['country'] = raw_input("Please enter your two-letter ISO country code. (eg. US, DE, JP, etc): ")
        print "Great.  Now take our short registration survey."
        metadata = {}
        for q in labels:
            metadata[q['id']] = raw_input(q['description'] + " ")
        args['metadata'] = metadata
        resp, code = self._post_json("api/team", args)
        if code != 200:
            print resp['message']
            return
        print "Cool! Now prove you're human."
        print resp['captcha']
        print "Yeah.  That's seriously a CAPTCHA."
        while True:
            captcha_resp = raw_input("Enter the 8 uppercase letters you see:")
            if self.verify(captcha_resp):
                break
            print "Oops! Try again."
        print "Great! You're done.  Go check your email for your password!  Then try iCTF.login()"

    def login(self, username, password):
        """
        Log into iCTF
        :param username: The team's username (email address)
        :param password: The team's password, sent via email
        :return: An auth token (Which is also saved to the iCTF object)
        """
        args = {}
        args['email'] = username
        args['password'] = password
        resp, code = self._post_json('api/login', args)
        if code != 200:
            raise RuntimeError(resp['message'])
        self._token = resp['token']
        return Team(self._token, username, game_url=self.game_url)

    def reset_password(self, team_email):
        args = {}
        args['team_email'] = team_email
        ret, code =  self._post_json("api/reset", args)
        return ret


class Team(object):
    """
    This object represents a logged-in iCTF team.
    This object can be used to perform actions on behalf of the team, such as submitting game artifacts
    """

    def __init__(self, token, email, game_url=DEFAULT_GAME_INTERFACE):
        self._token = token
        self._email = email
        self.game_url = game_url

    def __str__(self):
        return "<Team %s>" % self._email

    def _post_json(self,endpoint,j):
        # EG says: Why can't Ubuntu stock a recent version of Requests??? Ugh.
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        resp = requests.post(self.game_url + endpoint, auth=(self._token, ""), data=json.dumps(j), headers=headers)
        try:
            js = json.loads(resp.content)
            return js, resp.status_code
        except:
            return "", resp.status_code


    def _get_json(self,endpoint):
        assert (self._token is not None)
        resp = requests.get(self.game_url + endpoint, auth=(self._token, ""))
        try:
            js = resp.json()
        except:
            return "", resp.status_code
        return resp.json(), resp.status_code

    def _get_large_file_authenticated(self, endpoint, save_to):
	    r = requests.get(self.game_url + endpoint, auth=(self._token, ""), stream=True)
	    if r.status_code != 200:
	    	raise RuntimeError("Error downloading file!")
	    with open(save_to, 'wb') as f:
	        for chunk in r.iter_content(chunk_size=1024): 
	            if chunk: # filter out keep-alive new chunks
	                f.write(chunk)

    def get_vpn_config(self, fname):
    	"""
    	Download and save your team's VPN configuration.

    	The resulting file will be an OpenVPN configuration file, complete with certificate.
    	Just run it with 'openvpn [configfile]', and you're in!
    	(HINT: you might need to be root)
    	:param fname: File name to save the Tar-Gzipped service bundle to
    	:return: None
    	"""

    	resp,code = self._get_json("api/vpnconfig")
    	if code != 200 or not resp or not resp.has_key('vpnconfig'):
    		raise RuntimeError(resp['message'])
    	with open(fname,'wb') as f:
    		f.write(base64.b64decode(resp['vpnconfig']))

    def submit_service(self, name, service_bundle_fp):
        """
        Submit a service
        :param name: The service's name
        :param service_bundle_fp: Path to the Service Bundle.  See the documentation for details
        :return:
        """
        args = {}
        args['name'] = name
        
        with open(service_bundle_fp, 'rb') as f:
            args['payload'] = base64.b64encode(f.read())

        resp, code = self._post_json("api/service", args)
        if code != 200:
            raise RuntimeError(repr(resp))
        return resp['upload_id']

    def submit_dashboard(self, name, dashboard_bundle_fp):
        """
        Submit a dashboard for the dashboard contest!
        :param name: The dashboard's name
        :param dashboard_bundle_fp: Path to the Dashboard Bundle.  See the documentation for details
        :return:
        """
        args = {}
        args['name'] = name
        
        with open(dashboard_bundle_fp, 'rb') as f:
            args['archive'] = base64.b64encode(f.read())

        resp, code = self._post_json("api/dashboard", args)
        if code != 200:
            raise RuntimeError(repr(resp))
        print "Done."
    

    def get_service_status(self):
        """
        Get the service status and possible error message for the submitted service
        :return:
        """
        resp, code = self._get_json("api/service")
        if code == 200:
            return resp['uploads']
        else:
            raise RuntimeError(resp['message'])
    

    def get_vm_bundle(self, save_to):
    	"""
    	Download the team's VM bundle, and save it to the given file.

    	:param save_to: Path to save the bundle to
    	:return: None
    	"""
    	self._get_large_file_authenticated("api/vmbundle",save_to)


    def submit_flag(self, flags):
        """
        Submit a list of one or more flags
        :param flags: A list of flags
        :return: List containing a response for each flag, either:
        	"correct" | "ownflag" (do you think this is defcon?)
                      | "incorrect"
                      | "alreadysubmitted"
                      | "notactive",
                      | "toomanyincorrect",

        """
        resp, code = self._post_json("api/flag", {'flags': flags})
        if code == 200:
            return resp
        else:
        	return resp
    
    def get_targets(self, service):
        """
        Get a list of teams, their IP addresses, and the currently valid flag_ids.
        Your exploit should then try to exploit each team, and steal the flag with the given ID.

        You can/should use this to write scripts to run your exploits!

        :param service: The name or ID of a service (see get_service_list() for IDs and names)
        :return:
        """
        service_id = None
        if isinstance(service,str):
        	services = self.get_service_list()
        	svc = filter(lambda x: x['service_name'] == service, services)
        	if not svc:
        		raise RuntimeError("Unknown service " + service)
        	service_id = int(svc[0]['service_id'])
        else:
        	service_id = service
        resp, code = self._get_json("api/targets/" + str(service_id))
        if code == 200:
            return resp
        else:
            raise RuntimeError("Something went wrong getting targets.")
        

    def get_service_list(self):
    	"""
    	Returns the list of services, and some useful information about them.

    	"""
    	resp, code = self._get_json("api/services")
        if code == 200:
            return resp['services'][0].values()
        else:
            raise RuntimeError(repr(resp))


    def get_game_status(self):
    	"""
    	Return a dictionary containing game status information.
    	This will include:
    		- The scores of all teams
    		- Game timing information
    		- Information about services, including their status, number of exploitations, etc

    	This API is suitable for use in the creation of frontends.

    	"""
    	resp, code = self._get_json("api/status")
        if code == 200:
            return resp
        else:
            raise RuntimeError(resp['message'])


    def submit_service_vote(self, service_1, service_2, service_3):
    	"""
    	Submit your team's vote for the "Best service" prize!

    	:param service_1:
    	:param service_2:
    	:param service_3: Names of services, as listed in get_game_status() (in order, 1 = best)
    	:return: None

    	"""
    	resp, code = self._post_json("api/vote", {'service_1':service_1,'service_2':service_2,'service_3':service_3})
        if code == 200:
            return
        else:
            if not resp:
            	raise RuntimeError("An unknown error occurred submitting your vote")
            raise RuntimeError(resp['message'])



    def get_team_status(self):
        """
        Get your team's current status, including whether your
        team has been verified, metadata submitted, service submitted, etc
        :return: String
        """
        pass
