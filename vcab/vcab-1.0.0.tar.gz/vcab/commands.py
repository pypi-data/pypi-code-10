import os
import logging
from subprocess import list2cmdline
from vcp import VCP
from .message import Request, Response, MalformedMessageException

logger = logging.getLogger(__name__)

class CommandServer(object):
    def __init__(self, absinthe_config):
        self.__vcp = VCP()
        self.__absinthe_config = absinthe_config

    def process(self, message):
        logger.debug("Processing message: %s" % message)
        if message is None or len(message) < 2:
            return None
        try:
            request = Request.parse(message)
        except MalformedMessageException as e:
            return Response('Bad request', 400)

        command_handler_name = "cmd_%s" % request.command

        if not hasattr(self, command_handler_name):
            return Response("Bad request. Unknown command: '%s'" % request.command, 400, request.command)

        logger.debug("Handle command: '%s'" % request.command)

        try:
            cmd = getattr(self, command_handler_name)
            response = cmd(**request.params)
            response.command = request.command
            return response
        except Exception as e:
            logger.exception("Unhandled exception occured")
            return Response("Internal server error", 500, request.command)

    def cmd_get_projects(self):
        return Response(self.__vcp.projects.keys())

    def cmd_find_file(self, project, pattern, path):
        if project not in self.__vcp.projects:
            return Response("Project '%s' not found" % project, 404)

        if path not in self.__absinthe_config['paths']:
            return Response("Path '%s' not found" % path, 404)

        base_path = self.__absinthe_config['paths'][path]

        cmd = list2cmdline(['ag', '-g', pattern, '--nocolor'])

        files = []

        for repo_name in self.__vcp.projects[project].repositories:
            repo = self.__vcp.repositories[repo_name]
            repo_path = os.path.relpath(repo.path, base_path)
            result = repo.cmd(cmd)
            if not len(result):
                continue
            files += [os.path.join(repo_path, file.strip()) for file in result.split('\n') if len(file)]

        logger.debug("Files found: %s" % files)

        return Response(files)
