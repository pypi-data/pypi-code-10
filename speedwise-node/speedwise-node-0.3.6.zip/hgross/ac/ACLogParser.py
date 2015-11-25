"""
    Speedwise Assetto Corsa log parser
"""
import json
import os

__author__ = 'Henning Gross'
import traceback
import pickle
import time
import argparse
import re
import sys
import datetime
import codecs
import urllib

from hgross.racelog import ServerWatcher, Session
import hgross.racelog as racelog

CARLIST_REGEX = re.compile(u"^CARS=\\[(\".{0,}\"){0,}\\]")
TRACK_REGEX = re.compile(u"^TRACK=(.{0,})")
# previous to ac server 1.2 -> ENTRY_LIST_REGEX = re.compile(u"MODEL:\\ (.{0,})\\ \\((\\d{1,})\\)(.{0,})")
# previous: MODEL: ferrari_458_gt2 (1) [ []]
# now:      CAR: 0 bmw_m3_gt2 (0) [ []]  []  0 kg
ENTRY_LIST_REGEX =  re.compile("CAR:\\ (\\d{1,})\\ (.{1,})\\ \\((\\d{1,})\\).{0,}\\ kg")
CHAT_MESSAGE_REGEX = re.compile(u"CHAT\\ \\[(.{0,})\\]:\\ (.{0,})")
DRIVER_JOIN_AND_ASSIGNMENT_REGEX = re.compile(u"DRIVER\\ ACCEPTED\\ FOR\\ CAR\\ (\\d{1,})\\s{1,}DRIVER\\ ACCEPTED\\ FOR\\ CAR\\ ([^\\n]{0,})")
ASSETTO_CORSA_VERSION_REGEX = re.compile(u"Assetto\\ Corsa\\ Dedicated\\ Server\\ (.{0,})")
SERVER_START_TIME_REGEX =  re.compile(u"Assetto\\ Corsa\\ Dedicated\\ Server\\ .{0,}\\s{1,}Protocol\\ version:\\ \\d{1,}\\s{1,}([^\\n]{0,})")
NEXT_SESSION_HEADER_REGEX = re.compile(u"NextSession\\s{1,}SESSION:\\ (.{0,})\\s{1,}TYPE=(.{0,})\\s{1,}TIME=(\\d{1,})\\s{1,}LAPS=(\\d{1,})")
DRIVER_DISCONNECTED_REGEX = re.compile(u"^TCP\\ connection\\ (.{0,})\\ \\((\\d{1,})\\)\\ \\[(.{0,})\\ \\[\\]\\]\\ terminated")
#LAPTIME_REGEX = re.compile(u"Dispatching\\ TCP\\ message\\ to\\ .{0,}\\ \\((\\d{1,})\\)\\ \\[(.{0,})\\ \\[.{0,}\\]\\]\\s{1,}Car.onLapCompleted\\s{1,}LAP\\ (.{0,})\\ (\\d{1,5}:\\d{2,2}:\\d{3,3})")
# laptime regex changed with 1.3.4 (no more guid/car id available in the logs - thank you kunos ... not)
LAPTIME_REGEX = re.compile("Car.onLapCompleted\\s{0,}LAP\\ (.{0,})\\ (\\d{1,5}:\\d{2,2}:\\d{3,3})\\s{0,}SPLIT\\ COUNT:\\ (\\d{1,})\\s{0,}.{0,}\\s{0,}.{0,}\\s{0,}.{0,}Result.OnLapCompleted.\\ Cuts:\\ (\\d{1,})") # (driver_name, laptime, split_count, cuts)
STEAM_GUID_CORRECTION_REGEX = re.compile("Dispatching\\ TCP\\ message\\ to\\ .{0,}\\ \\((\\d{1,})\\)\\ \\[(.{0,})\\ \\[.{0,}\\]\\]")
SERVER_NAME_REGEX = re.compile(u"^CALLING\\ .{0,}\\?name=([^&]{0,})")
JSON_RESULTS_FILE_REGEX = re.compile("Saving\\ session\\ json\\ file:\\ (.{0,})\\s{0,}")


def create_racelog_session_from_ac_json(json_results_path, server_watcher, chat_messages):
    """
     Given the results.json file created by the acServer, we create a new racelog session object upon that
    :param json_results_path: the path to the results (json file)
    :param server_watcher: a server watcher instance
    :param chat_messages: a list of chat messages with the form ("nickname", "chat_msg")
    :return: some parsed data in te racelog form (list_of_driver_objects, list_of_vehicle_objects) or None, if the json file was not found
    """
    print (u"Processing json results at %s ..." % json_results_path)

    if not isinstance(server_watcher, racelog.ServerWatcher):
        raise ValueError("server_watcher has the wrong type (%s)" % str(type(server_watcher)))

    if not os.path.isfile(json_results_path):
        print ("ERROR: The given path for the results json file (%s) did not exist. Session data will not be complete." % json_results_path)
        return None
    with open(json_results_path, "r") as json_file:
        data = json.load(json_file)

        #server = ""
        #session_name = data["Type"]
        #track = data["TrackName"]
        #number_of_laps = data["RaceLaps"] # will be 0 for qualifying/practise ...

        json_drivers = set()   # we will fill this with Driver objects
        json_vehicles = set() # we will fill this with Vehicle objects

        driver_to_car = {} # mapping driver_guid -> car_id

        def add_driver(driver_object_json_data):
            """Adds a driver from a deserialized driver object to our json_drivers set."""
            name = driver_object_json_data["Name"]
            guid = driver_object_json_data["Guid"]

            if len(guid) == 0:
                # if no guid, then no valid driver.
                return None

            driver = racelog.Driver(guid, name)
            in_set = len([d for d in json_drivers if d.id == guid]) > 0
            if not in_set:
                json_drivers.add(driver)
                # only call on joined once
                server_watcher.on_driver_joined(driver)
            return driver

        def get_vehicle(car_id):
            """ Get the vehicle object for car_id from the vehicle set """
            for vehicle in json_vehicles:
                if vehicle.id == car_id:
                    return vehicle
            raise ValueError("car_id %s unknown" % str(car_id))

        def get_driver(driver_guid):
            """ Get the driver object by his guid from the drivers set"""
            for driver in json_drivers:
                if driver.id == driver_guid:
                    return driver
            raise ValueError("driver's guid %s unknown" % str(driver_guid))

        # first we create Driver objects iterating over everything because we don't trust kunos ;-)
        if "Laps" in data and data["Laps"] is not None:
            for lap in data["Laps"]:
                add_driver({"Name": lap["DriverName"], "Guid": lap["DriverGuid"]})

        if "Events" in data and data["Events"] is not None:
            for event in data["Events"]:
                if event.has_key("Type") and event["Type"] in ("COLLISION_WITH_ENV", "COLLISION_WITH_CAR"):
                    if event.has_key("Driver"):
                        add_driver(event["Driver"])

        if "Cars" in data and data["Cars"] is not None:
            for car in data["Cars"]:
                if "Driver" in car and car["Driver"] is not None:
                    add_driver(car["Driver"])

        if "Result" in data and data["Result"] is not None:
            for lap in data["Result"]:
                add_driver({"Name": lap["DriverName"], "Guid": lap["DriverGuid"]})

        # create vehicle objects
        if "Cars" in data and data["Cars"] is not None:
            for car in data["Cars"]:
                car_id = car["CarId"]
                car_model = car["Model"]
                ballast = car["BallastKG"]

                vehicle = racelog.Vehicle(car_id, car_model, ballast=ballast)
                json_vehicles.add(vehicle)
                server_watcher.on_vehicle_joined(vehicle)

        # then we just iterate through the driven laps; everytime we come across a driver that is not assigned to the car in our driver_to_car map, we create the appropriate AssignmentEvents
        if "Laps" in data and data["Laps"] is not None:
            for lap in data["Laps"]:
                car_id = lap["CarId"]
                car_model = lap["CarModel"]
                driver_name = lap["DriverName"]
                driver_guid = lap["DriverGuid"]
                laptime = int(lap["LapTime"])
                cuts = lap["Cuts"]
                sectors = [int(sector) for sector in lap["Sectors"]]

                vehicle = get_vehicle(car_id)
                driver = get_driver(driver_guid)

                # check if driver is assigned to vehicle
                if not driver.id in driver_to_car:
                    # assign
                    driver_to_car[driver.id] = car_id
                    server_watcher.on_driver_assigned_to_vehicle(vehicle, driver)
                elif driver.id in driver_to_car and driver_to_car[driver.id] != car_id:
                    print "reassigning ...", vehicle, driver
                    # unassign and reassign
                    assigned_car_id = driver_to_car[driver.id]
                    server_watcher.on_driver_unassigned_from_vehicle(get_vehicle(assigned_car_id), driver)
                    driver_to_car[driver.id] = vehicle.id
                    server_watcher.on_driver_assigned_to_vehicle(vehicle, driver)
                # else: driver is assigned to the right vehicle

                lap = racelog.Lap(laptime, vehicle, driver, sectors=sectors, cuts=cuts)
                server_watcher.on_lap_completed(lap)

        # gather collisions
        # Note: we currently do not care about the order of collisions and will therefore not know, in which lap a collision took place!
        #       we could fix this by observing the order of events through the log and then rearranging the events before committing them to the server_watcher
        if "Events" in data and data["Events"] is not None:
            for event in data["Events"]:
                if "Type" in event and event["Type"] is not None:
                    if event["Type"] == "COLLISION_WITH_ENV":
                        driver1 = get_driver(event["Driver"]["Guid"])
                        vehicle1 = get_vehicle(event["CarId"])
                        impact_speed = float(event["ImpactSpeed"])
                        server_watcher.on_collision_with_environment(driver1, vehicle1, impact_speed)
                    elif event["Type"] == "COLLISION_WITH_CAR":
                        driver1 = get_driver(event["Driver"]["Guid"])
                        vehicle1 = get_vehicle(event["CarId"])
                        driver2 = get_driver(event["OtherDriver"]["Guid"])
                        vehicle2 = get_vehicle(event["OtherCarId"])
                        impact_speed = float(event["ImpactSpeed"])
                        server_watcher.on_collision_with_car(driver1, vehicle1, driver2, vehicle2, impact_speed)

        # chat messages
        for driver_name, message in chat_messages:
            filtered_drivers = [x for x in json_drivers if x.name == driver_name]
            if len(filtered_drivers) > 0:
                driver = filtered_drivers[0]
                if len(filtered_drivers) > 1:
                    print (u"WARNING: Got two drivers with the same name (%s)! Assigning to %s" % (filtered_drivers, driver))
                server_watcher.on_chat_message(driver, message)

        # after that, unassign all vehicle/driver combos
        for driver_guid, car_id in driver_to_car.iteritems():
            server_watcher.on_driver_unassigned_from_vehicle(get_vehicle(car_id), get_driver(driver_guid))

        # driver left events
        for driver in json_drivers:
            server_watcher.on_driver_left(driver)

        return json_drivers, json_vehicles


def process_ac_log_input_stream(log_input_stream, server_watcher, webserver_client=None, log_to_file=False, filename_for_original_log="server_log.log", use_current_datetime=False, send_to_stdout=False, cwd=os.getcwd()):
    "Takes an input stream (like a log file or stdin) and parses it's content, which should be assetto corsa log outputs."
    # Collect sessions
    line_no = 0
    watcher = server_watcher
    started = False # will be False until the first NextSession was read
    cache = [] # list of lines to be cached
    server = racelog.Server(u"Unknown Assetto Corsa Server")
    track = None
    chat_messages = [] # list of tuples with the form ("nickname", "chat_message") that is cleared on each NextSession event.
    current_session = None
    collect_session_header = False
    collected_session_header_lines = [] # the lines after NEXT SESSION until we have our informations
    json_results_file_path = None # On "Saving results file ..." we store the path here. On "NextSession" we process and clear it. This overcomes a race condition.

    if log_to_file:
        f = codecs.open(filename_for_original_log, "w", "utf8")

    def retrieve_driver_guid(car_id, driver_name):
        """
            Tries to retrive a driver's guid by parsing the ENNTRY-page
        :param car_id: the car_id
        :param driver_name: the driver name (note: currently not used)
        :return: None, if failed or no webserver_client is used, steam_guid otherwise
        """
        # driver_name currently unused - maybe add some validation code
        if not webserver_client:
            return None
        entries = webserver_client.get_entries_for_car_id(car_id)
        e_orig = entries
        if entries:
            # filter out not connected entries (no ping)
            ping_index = entries[0].index(u"Ping")
            guid_index = entries[0].index(u"Guid")
            entries = [x for x in entries if not (x[ping_index] in ("Ping",))] # without the header line !
            if len(entries) > 2:
                print (u"WARNING: multiple connected players with name %s - choosing the first" % driver_name)
            out = None
            if len(entries) > 0:
                out = entries[0][guid_index]
            else:
                print(u"Failed to retrieve driver %s's guid from retrieved entry list. \nEntries orig: %s\n##################\n Entries: %s" % (driver_name, e_orig, entries))
            return out
        else:
            print (u"WARNING: didn't get any guids for driver %s" % driver_name)
            return None

    while True:
        try:
            read_line = log_input_stream.readline()
            if not read_line:
                print (u"EOF")
                break
            line = None
            try:
                line = unicode(read_line, 'windows-1252') # iso-8859-1 -> utf8
            except Exception as e:
                import chardet
                print ("%d: Could not read line %d: (%s)" % (line_no, line_no, str(e)))
                detected_charset = chardet.detect(read_line)
                print ("%d: Maybe this charset %s ... retry ..." % (line_no, detected_charset))
                try:
                    line = unicode(read_line, detected_charset['encoding'])
                    print "%d Could decode! Length: %d" % (line_no, len(line))
                except Exception as e2:
                    print ("%d: ERROR: Decoding with charset %s failed too - giving up to read line %d - message: %s" % (line_no, detected_charset["encoding"], line_no, e2))
                    line_no += 1
                    continue

            # -- line is unicode instance here
            if not line:
                break # EOF
            line_no += 1
            if send_to_stdout:
                sys.stdout.write(line)

            if log_to_file:
                f.write(line)

            if not started:
                # processing of the server start sequence
                if line.startswith(u"Server started"):
                    # the server startup header is through, so we use our cache to let some regex do their magic
                    cachedLines = "".join(cache)
                    cache = [] # clear cache
                    started = True

                    version_matcher = ASSETTO_CORSA_VERSION_REGEX.findall(cachedLines)
                    if version_matcher:
                        server.version = version_matcher[0]

                    start_time_matcher = SERVER_START_TIME_REGEX.findall(cachedLines)
                    server_start_time = None
                    if start_time_matcher:
                        start_time = start_time_matcher[0]
                        #start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                        server.start_time = start_time
                    if server_start_time:
                        server.start_time = server_start_time
                    watcher.on_server_started(server)

                # track
                track_match = TRACK_REGEX.findall(line)
                if track_match:
                    track = track_match[0]
                    watcher.on_track_changed(track)

                cache.append(line)

            else: # server is started
                if line.startswith(u"RESTARTING SESSION"):
                    # create new session
                    additional_data = current_session.additional_data
                    new_session = Session(server, current_session.session_name, track, datetime.datetime.now(), additional_data )
                    # submit old and new session
                    watcher.on_session_restarted(current_session, new_session)
                    current_session = new_session

                if line.startswith(u"CALLING"):
                    matches = SERVER_NAME_REGEX.findall(line)
                    if matches:
                        server_name = matches[0]
                        server_name = urllib.unquote_plus(server_name).decode('utf8')
                        server.server_name = server_name

                if line.startswith(u"Saving session json file"):
                    # read json data and create results right before the sessions ends (NextSession will follow)
                    matches = JSON_RESULTS_FILE_REGEX.findall(line)
                    if matches:
                        print ("Got json results file. (CWD: %s) Will wait until next session event to process it." % cwd)
                        json_results_file_path = os.path.join(cwd, matches[0])

                if line.startswith(u"NextSession"):
                    if current_session:
                        # we have a previous session - it ended
                        if json_results_file_path:
                            create_racelog_session_from_ac_json(json_results_file_path, server_watcher, chat_messages)
                        else:
                            print ("WARN: no json results were written by the acServer")
                        watcher.on_session_finished(current_session)
                        chat_messages = [] # clear cache
                        json_results_file_path = None # clear file path

                    # set the flag to collect the start session header lines
                    collect_session_header = True

                if collect_session_header:
                    collected_session_header_lines.append(line)

                # NextSession collection processing (end of collecting)
                if collect_session_header and line.startswith(u"LAPS="):
                    # we collected the header
                    collect_session_header = False
                    collected_content = "\n".join(collected_session_header_lines)
                    collected_session_header_lines = []
                    session_data_matcher = NEXT_SESSION_HEADER_REGEX.findall(collected_content)

                    if session_data_matcher:
                        session_name, session_type, session_time, laps = session_data_matcher[0]

                        # a new session started
                        if use_current_datetime:
                            start_time = datetime.datetime.now()
                        else:
                            # use server start time and append total time of previous session? IF i can find it?? TODO!
                            start_time = server.start_time

                        # create new session
                        additional_data = {"session_type": session_type, "session_time": session_time, "laps": laps}
                        current_session = racelog.Session(server, session_name, track, datetime.datetime.now(), additional_data=additional_data)
                        watcher.on_session_created(current_session)


            # we need to cache chat messages until session_finished and add them after the json processing to the server_watcher; we clear in on_finished
            if line.startswith(u"CHAT "):
                matcher = CHAT_MESSAGE_REGEX.findall(line)
                if matcher:
                    driver_name, message = matcher[0]
                    # we just cache the messages; they will be processed in the on session finished event (after we know all drivers)
                    chat_messages.append((driver_name, message))

        except Exception, _:
            print ("Something went wrong parsing a line " + str(line_no) + ":")
            print (traceback.format_exc())
    if log_to_file:
        f.close()

    # EOF - server stopped
    watcher.on_server_stopped(server)

session_no = 0 # TODO: dirty, get rid of global var

def main_func():
    sys.stdout = codecs.getwriter("utf8")(sys.stdout);

    argParser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description="Parses an Assetto Corsa log from file or stdin. For stdin simply specify 'stdin' as file name")
    argParser.add_argument("logfile", default="stdin", type=str, help="The logfile to parse and create separate logs from. If set to stdin, the stdin is used instead of a file.")
    argParser.add_argument("-p", action="store_true", help="Uses pickle to serialize internal data structures for each session and writes them in a .pickle file (only if more than 5 events happened!). Only supported for log files.")
    args = argParser.parse_args()

    if args.p:
         def pickler(session):
             global session_no
             serialized_session = pickle.dumps(session)
             event_cnt = len(session.events)
             if event_cnt > 5:
                 # log to file
                 with open("session_%d_%d_events.pickle" % (session_no, event_cnt), "w") as pickle_file:
                     pickle_file.write(serialized_session)
                     pickle_file.close()
             session_no += 1
         watcher = ServerWatcher(session_post_processor=pickler)
    else:
         watcher = ServerWatcher()

    if args.logfile == "stdin":
        print ("Reading log from stdin. Awaiting input ...")
        watcher.is_live = True
        process_ac_log_input_stream(sys.stdin, watcher, use_current_datetime=True, send_to_stdout=True)
    else:
        session_no = 0
        with open(args.logfile) as logfile:
            cwd =  os.path.dirname(logfile.name)
            process_ac_log_input_stream(logfile, watcher, log_to_file=True, cwd=cwd)
            logfile.close()
if __name__ == "__main__":
    main_func()