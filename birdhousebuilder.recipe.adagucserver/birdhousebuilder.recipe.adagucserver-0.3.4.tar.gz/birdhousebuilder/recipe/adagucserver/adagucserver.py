import os
import sys

def parse_output(output):
    lines = output.split('\n')
    content_type = "text/xml"
    start_line = 0
    # parse content-type/header
    for i,line in enumerate(lines):
        if 'content-type' in line.lower():
            content_type = line.split(':')[1]
            content_type = content_type.strip()
            start_line = i+2
            break
    data = '\n'.join(lines[start_line:-1])
    return content_type,data

def app(environ, start_response):
    from subprocess import check_output, STDOUT
    data = None
    try:
        # fake cgi parameters
        """
        QUERY_STRING       
        REQUEST_METHOD     
        CONTENT_TYPE       
        CONTENT_LENGTH     

        SCRIPT_FILENAME 
        SCRIPT_NAME     
        REQUEST_URI        
        DOCUMENT_URI       
        DOCUMENT_ROOT      
        SERVER_PROTOCOL    

        GATEWAY_INTERFACE  CGI/1.1;
        SERVER_SOFTWARE    

        REMOTE_ADDR        
        REMOTE_PORT        
        SERVER_ADDR        
        SERVER_PORT        
        SERVER_NAME        
        """
        params = [
            'QUERY_STRING',
            'REQUEST_METHOD',
            'SERVER_PROTOCOL',
            'SERVER_SOFTWARE',
            'REMOTE_ADDR',
            'SERVER_PORT',
            'SERVER_NAME'
            ]

        env = os.environ.copy()
        for param in params:
            env[param] = environ[param]
        env['GATEWAY_INTERFACE'] = 'CGI/1.1'

        ON_POSIX = 'posix' in sys.builtin_module_names

        # run adagucserver
        output = check_output(['adagucserver'], stderr=STDOUT, bufsize=8192, close_fds=ON_POSIX, env=env)
        content_type, data = parse_output(output)
        start_response("200 OK", [
            ("Content-Type", content_type),
            #("Content-Length", str(len(data)))
            ])
    except Exception as e:
        data = "Message:<br/>"
        data += str(e.message)

        # TODO: returncode 143 = application was killed
            
        start_response("200 OK", [
            ("Content-Type", "text/html"),
            ("Content-Length", str(len(data)))
            ])
    return iter([data])
