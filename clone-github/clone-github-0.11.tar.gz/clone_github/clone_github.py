#!/usr/bin/env python

import json, urllib, os, sys
from optparse import OptionParser

#####################################################################

def main():

    parser = OptionParser()
    parser.add_option("-o", "--org", dest="org", help="Github.com organization name. Assumes Oauth user if omitted.")
    parser.add_option("-u", "--user", dest="user", help="Github.com user name. Assumes Oauth user if omitted.")
    parser.add_option("-t", "--token", dest="token", help="OAuth Access Token.")
    parser.add_option("-p", "--private", action="store_true", dest="private", default=False,  help="List only Private repos. Default is Public.")
    parser.add_option("-r", "--run", action="store_true", dest="run", default=False,  help="Execute changes. Default is Dry Run.")
    (options, args) = parser.parse_args()


    #####################################################################

    command = ''
    url="https://api.github.com/"

    #####################################################################

    if options.org:
      # https://developer.github.com/v3/repos/#list-organization-repositories
      url += "orgs/" + options.org + "/repos?type="
    elif options.user:
      # https://developer.github.com/v3/repos/#list-user-repositories
      url += "users/" + options.user + "/repos?type=all&"
    else:
      # https://developer.github.com/v3/repos/#list-your-repositories
      url += "user/repos?affiliation=owner&visibility="

    if options.private:
      url += "private"
    else:
      url += "public"

    if options.token:
      url += "&access_token=" + options.token

    url += "&per_page=100&page="


    if options.run == False:
     command += 'echo '
    else:
      command += 'git clone '


    #print url

    #####################################################################

    try:
      page = 1
      jdata = json.load(urllib.urlopen('{}{}'.format(url,page)))

      while len(jdata) > 0:
        print ''
        print 'Page: {} Count: {}'.format(page, len(jdata))
        print ''
        for o in jdata:
          os.system('{} {}'.format(command, o['clone_url']))
        page += 1
        jdata = json.load(urllib.urlopen('{}{}'.format(url,page)))
    except Exception as e:
      parser.print_help()

#####################################################################

if __name__ == "__main__":
  try:
    main ()
  except KeyboardInterrupt:
    print 'Execution aborted.'
