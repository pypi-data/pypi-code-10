#!/usr/bin/python

import os
import sys
import getopt
import tempfile
import pytumblr
import ConfigParser

from subprocess import call

skellington = """[Tumblr]
blog:
consumer_key:
consumer_secret:
token:
token_secret:
"""

def usage(fd = sys.stdout):
    print >>fd, ("%s [-aqivlChm] [-b blog] [-f config] [-d date] [-s state] "
          "[-t tags] [-u url] [-T title] [-c caption] [-e excerpt] "
          "[-A author] [FILE...]" % sys.argv[0])

def main():
    config = os.environ.get("TMBLR_CONFIG") or os.path.expanduser('~/.tmblr')

    blog = None
    kind = 'text'
    post = {}
    editor = os.environ.get("EDITOR", "ed")

    try:
        opts, args = getopt.getopt(sys.argv[1:], "aqivlChb:f:d:s:t:T:u:c:e:m")
    except getopt.GetoptError as err:
        print >>sys.stderr, str(err)
        usage(sys.stderr)
        sys.exit(1)
    for o, a in opts:
        if o == '-h':
            usage()
            exit(0)
        elif o == '-b':
            blog = a
        elif o == '-f':
            config = a
        elif o == '-s':
            post['state'] = a
        elif o == '-t':
            post['tags'] = str.split(a, ",")
        elif o == '-d':
            post['date'] = a
        elif o == '-m':
            post['format'] = 'markdown'
        elif o == '-a':
            kind = 'audio'
        elif o == '-q':
            kind = 'quote'
        elif o == '-i':
            kind = 'photo'
        elif o == '-v':
            kind = 'video'
        elif o == '-l':
            kind = 'link'
        elif o == '-C':
            kind = 'chat'
        elif o == '-c':
            post['caption'] = a
            if a == ".":
                with tempfile.NamedTemporaryFile(suffix=".tmp") as temp:
                    temp.write("caption")
                    temp.flush()
                    call([editor, temp.name])
                    post['caption'] = temp.read()
        elif o == '-T':
            post['title'] = a
        elif o == '-u':
            post["source_url"] = a
        elif o == '-e':
            post["excerpt"] = a
        elif o == '-A':
            post['author'] = a

    if not os.path.exists(config):
        with open(config, 'w') as f:
            f.write(skellington)
        print >>sys.stderr, "put blog name and silly tokens in %s" % config
        sys.exit(1)

    parser = ConfigParser.ConfigParser()
    parser.read(config)

    if(not blog): blog = parser.get("Tumblr", "blog")

    client = pytumblr.TumblrRestClient(
        parser.get('Tumblr', 'consumer_key'),
        parser.get('Tumblr', 'consumer_secret'),
        parser.get('Tumblr', 'token'),
        parser.get('Tumblr', 'token_secret')
    )

    response = None
    if(kind == "text" or kind == "chat" or kind == "quote"):
        if "caption" in post: post.pop('caption')
        if(len(args) < 1):
            with tempfile.NamedTemporaryFile(suffix=".tmp") as temp:
                call([editor, temp.name])
                post['body'] = temp.read()
        elif args[0] == '-':
            post['body'] = sys.stdin.read()
        else:
            with open(args[0], 'r') as f:
                post['body'] = f.read()
        if(kind == "chat"):
            post['conversation'] = post.pop('body')
            response = client.create_chat(blog, **post)
        elif(kind == "quote"):
            post['quote'] = post.pop('body')
            response = client.create_quote(blog, **post)
        else:
            response = client.create_text(blog, **post)
    elif(kind == "photo"):
        post['data'] = args
        response = client.create_photo(blog, **post)
    elif(kind == "audio"):
        if(len(args) < 1):
            print >>sys.sterr, "No audio file specified"
            sys.exit(1)
        post['data'] = args[0]
        response = client.create_audio(blog, **post)
    elif(kind == "video"):
        if(len(args) < 1):
            print >>sys.sterr, "No video file specified"
            sys.exit(1)
        post['data'] = args[0]
        response = client.create_video(blog, **post)
    elif(kind == "link"):
        if(len(args) < 1):
            print >>sys.sterr, "No link specified"
            sys.exit(1)
        post['url'] = args[0]
        post['description'] = post.pop('caption')
        response = client.create_link(blog, **post)
    if(response and 'id' in response):
        print("http://%s.tumblr.com/%s" % (blog, response['id']))
    elif(response and 'response' in response):
        if('errors' in response['response']):
            print >>sys.stderr, str.join("\n", response['response']['errors'])
        elif('meta' in response and 'msg' in response['meta']):
            print >>sys.stderr, "Bad mojo: %s" % response['meta']['msg']
        sys.exit(1)

if __name__ == "__main__":
    main()

