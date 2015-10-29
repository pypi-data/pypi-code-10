import sys
import datetime
import os
import time
import cgi
import itertools
import inspect
import shutil
from egat.loggers.test_logger import TestLogger
from egat.loggers.test_logger import LogLevel
from egat.test_result import TestResult
from egat.test_runner_helpers import TestFunctionType
from itertools import groupby
from Queue import Queue
from Queue import Empty
from pkg_resources import Requirement, resource_filename, DistributionNotFound
from multiprocessing import Lock

class TestResultType():
    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"


class HTMLWriter():

    @staticmethod
    def copy_resources_to_log_dir(log_dir):
        """Copies the necessary static assets to the log_dir and returns the path 
        of the main css file."""
        css_path = resource_filename(Requirement.parse("egat"), "/egat/data/default.css")
        header_path = resource_filename(Requirement.parse("egat"), "/egat/data/egat_header.png")
        shutil.copyfile(css_path, log_dir + "/style.css")
        shutil.copyfile(header_path, log_dir + "/egat_header.png")

        return log_dir + os.sep + "style.css"

    @staticmethod
    def write_test_results(test_results, start_time, end_time, fp, css_path):
        """Takes a list of TestResult objects and an open file pointer and writes 
        the test results as HTML to the given file."""

        css_str = '<link rel="stylesheet" href="%s" type="text/css">' % css_path
        title = "Test Run %s" % start_time.strftime("%m-%d-%y %H:%I %p")

        html = """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="utf-8"/>
                    <title>%s</title>
                    %s
                    <script type="text/javascript">
                        function toggleFuncDetails(id) {
                            // check to see if we are already showing the traceback
                            var testResultRow = document.querySelector("tr[id='" + id + "-result']")
                            var detailsRow = document.querySelector("tr[id='" + id + "-details']")
                            var hiddenDetailsDiv = document.querySelector("div[id='" + id + "-hidden-details']")

                            if (detailsRow === null) {
                                // the details are hidden; show it.
                                var details = hiddenDetailsDiv.innerHTML
                                detailsRow = document.createElement('tr')
                                detailsRow.setAttribute('id', id + "-details")
                                detailsRow.innerHTML = "<td></td><td></td><td class='details' colspan='4'>" + details + "</td>"
                                testResultRow.parentNode.insertBefore(detailsRow, testResultRow.nextSibling)
                            } else {
                                // the details are already showing; hide them.
                                detailsRow.parentNode.removeChild(detailsRow)
                            }
                        }

                        function toggleClassDetails(button, id) {
                            var classRow = document.querySelector("tr[id='" + id + "-class']")
                            var rowsToHide = []

                            if (classRow.className.indexOf("collapsed") > -1) {
                                // classRow is collapsed. Expand it.
                                button.textContent = "[-]"
                                classRow.className = classRow.className.replace("collapsed", "")
                                var currentNode = classRow.nextElementSibling
                                while (currentNode.className == null ||
                                    currentNode.className.indexOf("class-header") == -1) {
                                    currentNode.style.display = "table-row"
                                    currentNode = currentNode.nextElementSibling
                                }
                            } else {
                                // classRow is expanded. Collapse it.
                                button.textContent = "[+]"
                                classRow.className = classRow.className + " collapsed"
                                var currentNode = classRow.nextElementSibling
                                while (currentNode.className == null ||
                                    currentNode.className.indexOf("class-header") == -1) {
                                    currentNode.style.display = "none"
                                    currentNode = currentNode.nextElementSibling
                                }
                            }
                        }
                    </script>
                </head>
                <body>""" % (title, css_str)

        html += """
            <div id="header-image">
                <img src="egat_header.png"/>
            </div>
            <div class="header">
                <h1 id="title">%s</h1> 
                <h3>Start time: %s</h3>
                <h3>End time: %s</h3>
                <h3>Duration: %s</h3>
            </div>
        """  % (
            title,
            start_time.strftime("%m-%d-%y %H:%M:%S"),
            end_time.strftime("%m-%d-%y %H:%M:%S"),
            str(end_time - start_time).split('.', 2)[0]
        )

        results = HTMLWriter.dump_queue(test_results)

        # Calculate totals
        successes = len(filter(lambda r: r.status == TestResultType.SUCCESS, results))
        failures = len(filter(lambda r: r.status == TestResultType.FAILURE, results))
        skipped = len(filter(lambda r: r.status == TestResultType.SKIPPED, results))

        # Add totals row
        html += """
            <table class='totals-table'>
                <td>Successes</td>
                <td class="success" colspan="1">%d</td>
                <td>Failures</td>
                <td class="failure" colspan="1">%d</td>
                <td>Skipped</td>
                <td class="skipped" colspan="1">%d</td>
            </table>
            <br />""" % (successes, failures, skipped)

        # Group tests by class and environment
        tests_by_class = {}
        for result in results:
            tests_by_env = tests_by_class.get(result.full_class_name(), {})
            env_str = HTMLWriter.hashable(result.environment)
            results = tests_by_env.get(env_str, []) 
            results.append(result)
            tests_by_env[env_str] = results
            tests_by_class[result.full_class_name()] = tests_by_env

        html += "<table class='results-table'>"

        # Add table headings
        html += """
            <tr>
                <th></th>
                <th></th>
                <th>Function</th>
                <th>Status</th>
                <th>Thread</th>
                <th>Details</th>
            </tr>"""

        i = 0
        for class_name, tests_by_env in tests_by_class.items():
            # find class totals
            all_results = list(itertools.chain(*tests_by_env.values()))
            successes = len(filter(lambda r: r.status == TestResultType.SUCCESS, all_results))
            failures = len(filter(lambda r: r.status == TestResultType.FAILURE, all_results))
            skipped = len(filter(lambda r: r.status == TestResultType.SKIPPED, all_results))

            row_classes = "class-header collapsed"
            if failures > 0:
                row_classes += " failure"
            elif skipped > 0:
                row_classes += " skipped"

            # Add class header
            html += """
                <tr id="%s-class" class="%s">
                    <td class="expand-collapse-btn">
                        <a onclick="toggleClassDetails(this, %s)">[+]</a>
                    </td>
                    <td colspan="5">
                        <span style="float:left;">
                            %s                        
                        </span>
                        <span style="float:right;">
                            Successes:
                            %d
                            Failures:
                            %d
                            Skipped:
                            %d
                        </span>
                    </td>
                </tr>
                """ % (i, row_classes, i, class_name, successes, failures, skipped)
            i += 1

            for env_str, test_results in tests_by_env.items():
                if test_results[0].environment:
                    # Add environment header
                    html += """
                        <tr class="environment-header" style="display:none;">
                            <td></td>
                            <td colspan="5">%s</td>
                        </tr>""" % test_results[0].environment_string()

                for result in test_results:
                    # Format the traceback
                    traceback_str = ""
                    if result.traceback:
                        traceback_str = cgi.escape(result.traceback)
                        traceback_str = traceback_str.replace(' ', '&nbsp;')
                        traceback_str = traceback_str.replace('\n', '<br />')

                    # Format the resource_groups
                    def print_resource_groups(rgroup):
                        if inspect.isclass(rgroup):
                            return rgroup.__name__
                        else:
                            return str(rgroup)
                    resource_group_str = map(print_resource_groups, result.resource_groups)

                    row = """
                        <tr id="%s-result" class="test-result" style="display:none">
                            <td class='empty-cell'></td>
                            <td class='empty-cell'></td>
                            <td class='function-name'>%s</td>
                            <td class='%s'>%s</td>
                            <td class='thread-num'>%s</td>
                            <td class="details-btn">
                                <a onclick="toggleFuncDetails(%s)">Details</a>
                            </td>
                            <td style="display:none">
                                <div id="%s-hidden-details" class='details'>
                                    Resource Groups: %s<br/>
                                    Execution Groups: %s<br/>
                                    Start Time: %s<br />
                                    End Time: %s<br />
                                    Duration: %s<br />
                                    %s
                                </div>
                            </td>
                        </tr>
                        """ % (i, 
                               result.func.__name__, 
                               result.status, 
                               result.status, 
                               result.thread + 1, 
                               i, 
                               i, 
                               resource_group_str, 
                               result.execution_groups, 
                               result.start_time.strftime("%m-%d-%y %H:%M:%S"),
                               result.end_time.strftime("%m-%d-%y %H:%M:%S"),
                               str(result.end_time - result.start_time),
                               traceback_str)

                    html += row
                    i += 1

        html += "</table></body></html>"

        fp.write(html)

    @staticmethod
    def dump_queue(queue):
        """
        Empties all pending items in a queue and returns them in a list.
        """
        result = []

        try:
            while True:
                item = queue.get_nowait()
                result.append(item)
        except: Empty

        return result

    @staticmethod
    def hashable(d):
        """Takes a dictionary and returns a hashable string representing it."""
        return "%^&*|".join(map(str, d.keys() + d.values()))

class HTMLLogger(TestLogger):
    """A logger that writes test output to an interactive HTML page."""
    out = None
    results = None
    current_tests = None
    start_time = None
    end_time = None
    test_title = None
    css_path = None
    failed_test_count = None
    lock = None

    def __init__(self, log_dir=None, log_level=LogLevel.ERROR, css_path=None):
        if log_dir: 
            log_dir = os.path.abspath(log_dir)
        if css_path: 
            css_path = os.path.abspath(css_path) 

        TestLogger.__init__(self, log_dir=log_dir, log_level=log_level)
        self.css_path = css_path
        self.failed_test_count = 0
        self.lock = Lock()

    def startingTests(self):
        if not self.log_dir: self.log_dir = "."

        # Set up the log file
        self.start_time = datetime.datetime.now()
        self.log_dir = self.log_dir.rstrip(os.sep)
        self.test_title = "Test Run %s" % self.start_time.strftime("%m-%d-%y %H:%M:%S")
        self.log_dir += "%s%s" % (os.sep, self.test_title.replace(':', '.'))
        os.mkdir(self.log_dir)
        log_name = "%s%sresults.html" % (self.log_dir, os.sep)
        self.out = open(log_name, 'w')

        self.results = Queue()
        self.current_tests = {}
    
    def finishedTests(self):
        self.end_time = datetime.datetime.now()
        if self.css_path:
            shutil.copyfile(self.css_path, self.log_dir + "/style.css")
        else:
            self.css_path = HTMLWriter.copy_resources_to_log_dir(self.log_dir)
        HTMLWriter.write_test_results(
            self.results, 
            self.start_time, 
            self.end_time, 
            self.out, 
            css_path="style.css" # <-- this is hardcoded to work around a bug in Firefox on Windows where CSS loaded from the filesystem must use a relative path.
        )

        return self.failed_test_count

    def runningTestFunction(self, class_instance, func, func_type=TestFunctionType.TEST, thread_num=None):
        result = TestResult(class_instance, func, thread=thread_num)
        result.start_time = datetime.datetime.now()
        with self.lock:
            self.current_tests[(class_instance, func, thread_num)] = result

    def finishedTestFunction(self, class_instance, func, func_type=TestFunctionType.TEST, thread_num=None):
        with self.lock:
            result = self.current_tests.pop((class_instance, func, thread_num))
            # Don't log results for setup and teardown unless they fail
            if func_type == TestFunctionType.TEST or result.status == TestResultType.FAILURE:
                result.end_time = datetime.datetime.now()
                if not result.status: result.status = TestResultType.SUCCESS
                self.results.put(result)

        if self.log_level >= LogLevel.DEBUG:
            self.log_debug_info(class_instance, func)

    def skippingTestFunction(self, class_instance, func, func_type=TestFunctionType.TEST, thread_num=None):
        # Don't log results for setup and teardown unless they fail
        if func_type == TestFunctionType.TEST:
            with self.lock:
                result = TestResult(class_instance, func, status=TestResultType.SKIPPED, thread=thread_num)
                result.start_time = datetime.datetime.now()
                result.end_time = datetime.datetime.now()
                self.results.put(result)

    def foundException(self, class_instance, func, e, tb, func_type=TestFunctionType.TEST, thread_num=None):
        with self.lock:
            self.failed_test_count += 1
            result = self.current_tests[(class_instance, func, thread_num)]
        result.status = TestResultType.FAILURE
        result.error = e
        result.traceback = tb

        if self.log_level >= LogLevel.INFO:
            self.log_debug_info(class_instance, func)
