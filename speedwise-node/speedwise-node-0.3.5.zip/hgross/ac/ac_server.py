import json
import pickle
import threading
import uuid
import os
import subprocess
import shutil
import errno
import time

from hgross.ac.ACLogParser import process_ac_log_input_stream
from hgross.ac.ACRequestTools import ACWebServerClient
from hgross.racelog import ServerWatcher
from hgross.speedwise.speedwise_client import SpeedwiseClient
from hgross.speedwise.util import ProcessTerminationNotifier, ensure_dir


__author__ = 'Henning Gross'

SERVER_WORKING_DIR_FILENAME_PREFIX = "ACServer_" # guid will be suffixed
SERVER_PIDFILE_NAME = "PROC_PID"
SERVER_PRESET_INDICATOR_NAME = "USED_PRESET"
SERVER_INFO_JSON_NAME = "SPEEDWISE-INFO.json"

MINORATING_PATH = "MinoRating" + os.path.sep + "current" # relative path to the base ac dir
MINORATING_DEFAULT_CONFIG_NAME = "MinoRatingPlugin.exe.config_DEFAULT" # relative to the minorating dir
MINORATING_CONFIG_NAME = "MinoRatingPlugin.exe.config" # relative to the minorating dir
MINORATING_EXECUTABLE = "MinoRatingPlugin.exe"

if os.name == 'nt':
    DEDICATED_SERVER_BINARY_FILENAME = "acServer.exe"
elif os.name == 'posix':
    DEDICATED_SERVER_BINARY_FILENAME = "acServer"
else:
    raise BaseException("Unsupported operating system")


class KeepAliveSender(threading.Thread):
    def __init__(self, speedwise_client, server_guid):
        threading.Thread.__init__(self)
        assert(isinstance(speedwise_client, SpeedwiseClient))
        self.client = speedwise_client
        self.server_guid = server_guid
        self.started = True
        self.keep_alive_interval = 2.5 * 60 # every 2.5 minutes

    def stop_keep_alive(self):
        self.started = False

    def run(self):
        last_time = 0
        while self.started:
            if last_time + self.keep_alive_interval < time.time():
                result = self.client.send_keep_alive(self.server_guid)
                print (u"Sent keep alive to server. Result: %s" % result)
                last_time = time.time()
            time.sleep(2)

class ACServerStdoutProcessingThread(threading.Thread):
    SESSION_DATA_DIR_NAME = "SpeedwiseData"
    SESSION_UNPROCESSED_DIR_NAME = "todo"
    SESSION_PROCESSED_DIR_NAME = "sent"

    def __init__(self, process, dedicated_server):
        threading.Thread.__init__(self)
        self.dedicated_server = dedicated_server

        # create the pickler to save the sessions and process outputs
        def pickler(session):
            todo_folder = dedicated_server.workingDir + os.path.sep + ACServerStdoutProcessingThread.SESSION_DATA_DIR_NAME + os.path.sep + ACServerStdoutProcessingThread.SESSION_UNPROCESSED_DIR_NAME + os.path.sep
            processed_folder = dedicated_server.workingDir + os.path.sep + ACServerStdoutProcessingThread.SESSION_DATA_DIR_NAME + os.path.sep + ACServerStdoutProcessingThread.SESSION_PROCESSED_DIR_NAME + os.path.sep
            ensure_dir(todo_folder)
            ensure_dir(processed_folder)
            serialized_session = pickle.dumps(session)

            # log to file
            event_cnt = len(session.events)
            pickle_file_name = todo_folder + u"session_%s_%d_events.pickle" % (str(session.uuid), event_cnt)
            with open(pickle_file_name, "w") as pickle_file:
                pickle_file.write(serialized_session)
                pickle_file.close()
            # process data
            dedicated_server.speedwise_client.process_session_data(todo_folder, processed_folder)

        self.speedwise_client = dedicated_server.speedwise_client
        self.process = process
        self.webserver_client = dedicated_server.webserver_client
        self.standard_logfile_path = dedicated_server.ac_log_file_path
        self.server_watcher = ServerWatcher(is_live=True, session_post_processor=pickler)

    def run(self):
        # start keep alive
        ka_sender = KeepAliveSender(self.speedwise_client, self.dedicated_server.guid)
        ka_sender.start()

        #log_input_stream, server_watcher, webserver_client=None, log_to_file=False, filename_for_original_log="server_log.log", use_current_datetime=False, send_to_stdout=False)
        process_ac_log_input_stream(self.process.stdout, self.server_watcher, webserver_client=self.webserver_client, log_to_file=True, filename_for_original_log=self.standard_logfile_path, use_current_datetime=True, send_to_stdout=False, cwd=self.dedicated_server.workingDir)

        # stop keep alive
        ka_sender.stop_keep_alive()

def _mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

class ACDedicatedServer():
    STANDARD_LOG_FILE_NAME = "ac_server.log"

    def __init__(self, serverConfig, wrapperConfig):
        self.lock = threading.Lock()
        self.serverConfig = serverConfig
        self.wrapperConfig = wrapperConfig
        self.guid = uuid.uuid4()
        self.process = None # indicates if a server is running
        self.workingDir = self.wrapperConfig.DEDICATED_SERVER_WORKSPACES_DIRECTORY + os.path.sep + SERVER_WORKING_DIR_FILENAME_PREFIX + str(self.guid)

        http_port = self.serverConfig.server_cfg.get("SERVER", "HTTP_PORT")
        self.webserver_client = ACWebServerClient("127.0.0.1", http_port, maxAge=0)
        self.speedwise_client = SpeedwiseClient(self.wrapperConfig.speedwise_server_hostname, self.wrapperConfig.speedwise_server_port, self.wrapperConfig.speedwise_server_id, self.wrapperConfig.speedwise_server_secret)

        self.ac_log_file_path = self.workingDir + os.path.sep + ACDedicatedServer.STANDARD_LOG_FILE_NAME

    def start_server(self):
        if self.isRunning():
            print ("ACServer: startServer() ignored - startServer() ignored")
            return

        with self.lock:
            self._createWorkingDirectory()
            executableFullPath = self.workingDir + os.path.sep + DEDICATED_SERVER_BINARY_FILENAME
            #os.chdir(self.workingDir)
            print ("Starting server in working directory %s" % self.workingDir)
            process = subprocess.Popen([executableFullPath], cwd=self.workingDir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            pid = str(process.pid)
            print ("Server PID is %s" % pid)

            preset_file_path = self.workingDir + os.path.sep + SERVER_PRESET_INDICATOR_NAME
            print ("Writing PRESET-file to %s" % str(preset_file_path))
            with open(preset_file_path, "w") as preset_file:
                preset_file.write(self.serverConfig.preset_name)
                preset_file.close()
            assert os.path.isfile(preset_file_path)

            pid_file_path = self.workingDir + os.path.sep + SERVER_PIDFILE_NAME
            print ("Writing PID-file to %s" % str(pid_file_path))
            with open(pid_file_path, "w") as pid_file:
                pid_file.write(str(pid))
                pid_file.close()

            info_json_file_path = self.workingDir + os.path.sep + SERVER_INFO_JSON_NAME
            print ("Writing INFO json file to %s" % str(info_json_file_path))
            with open(info_json_file_path, "w") as info_json_file:
                server_info = {
                    "server_id": self.wrapperConfig.speedwise_server_id,
                    "preset": self.serverConfig.preset_name,
                    "server_pid": str(pid)
                }
                info_json_file.write(json.dumps(server_info))
                info_json_file.close()

            # check if we want to start MR
            mr_process = None
            if self.serverConfig.is_minorating_activated():
                # start mr instance for this server
                minorating_exectuable = MINORATING_EXECUTABLE
                mr_dir_path = self.workingDir +  os.path.sep + MINORATING_PATH

                minorating_executable_path = mr_dir_path + os.path.sep + minorating_exectuable
                exec_list = [minorating_executable_path]

                if os.name == 'posix':
                    # prepend mono
                    exec_list = ["mono", minorating_executable_path]

                with open(os.devnull, 'w') as dnull:
                    # TODO: check if MR could be started (result code)
                    mr_process = subprocess.Popen(exec_list, cwd=mr_dir_path, stderr=dnull, stdout=dnull)

            def onTerminationCallback():
                os.remove(pid_file_path)
                if self.serverConfig.is_minorating_activated():
                    if mr_process is not None:
                        print ("Killing MinoRating ...")
                        mr_process.terminate()

            notifier = ProcessTerminationNotifier(process, onTerminationCallback)
            notifier.start()
            self.process = process
            print ("Starting processing ...")
            processing_thread = ACServerStdoutProcessingThread(process, self)
            processing_thread.start()

    def _start_minorating_process(self):
        pass

    def stop_server(self):
        with self.lock:
            if self.process is None:
                print ("ACServer: Server not running - stopServer() ignored.")
                return
            #if self.process.poll() is not None:
            print ("ACServer: Terminating server process %s" % str(self.process))
            self.process.terminate()

    def isRunning(self):
        with self.lock:
            return self.process is not None and self.process.poll() is None

    def _createWorkingDirectory(self):
        # copy all base dedicated server files
        src = self.wrapperConfig.DEDICATED_SERVER_BASE_DIRECTORY
        dst = self.workingDir
        try:
            shutil.copytree(src, dst)
        except OSError as exc: # python >2.5
            if exc.errno == errno.ENOTDIR:
                shutil.copy(src, dst)
            else:
                raise

        # ensure cfg folder
        try:
            _mkdir_p(self.workingDir + os.path.sep + 'cfg')
        except:
            pass

        # remove any config files
        entry_file_path = self.workingDir + os.path.sep + 'cfg' + os.path.sep + 'entry_list.ini'
        server_cfg_file_path = self.workingDir + os.path.sep + 'cfg' + os.path.sep + 'server_cfg.ini'

        try:
            os.remove(entry_file_path)
        except:
            pass

        try:
            os.remove(server_cfg_file_path)
        except:
            pass

        # write config to cfg dir
        self.serverConfig.exportConfig(self.workingDir + os.path.sep + "cfg")

        # MINORATING config
        if self.serverConfig.is_minorating_activated():
            # find trust token
            trust_token = self.serverConfig.server_cfg.get("MINORATING", "TRUST_TOKEN")

            # create initial config from default config
            default_config_path = self.workingDir + os.path.sep + MINORATING_PATH + os.path.sep + MINORATING_DEFAULT_CONFIG_NAME
            config_path = self.workingDir + os.path.sep + MINORATING_PATH + os.path.sep + MINORATING_CONFIG_NAME

            # copy trust token to config
            with open(default_config_path, "r") as default_cfg:
                with open(config_path, "w") as cfg:
                    for line in default_cfg.readlines():
                        if trust_token is not None and len(trust_token) > 0:
                            line = line.replace('<add key="server_trust_token" value=""/>', '<add key="server_trust_token" value="%s"/>' % trust_token)
                        cfg.write(line)
                    cfg.close()
                default_cfg.close()
