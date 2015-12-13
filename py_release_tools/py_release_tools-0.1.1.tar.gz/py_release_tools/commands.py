import os
import re
import sys
from io import BytesIO
from distutils import log
from distutils.cmd import Command
from subprocess import check_output
from distutils.errors import DistutilsError


def simple_call(cmd):
    return check_output(cmd.split(" "))


class SimpleCommand(Command):
    """Default behavior for simple commands
    """

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def install_requires(self):
        if self.distribution.install_requires:
            self.distribution.fetch_build_eggs(
                    self.distribution.install_requires)

        if self.distribution.tests_require:
            self.distribution.fetch_build_eggs(
                    self.distribution.tests_require)

    def run(self):
        self.install_requires()
        self._run()


class IncrementSemanticVersion(SimpleCommand):
    """Increment Semantic Version and Commmit to Git

    Version incrementing uses semantic versioning. This command accepts -M or
    --major, -m or --minor to increment a major or minor release. If no flags
    are passed then a patch release is created.
    """

    user_options = [
        ("major", "M", "increment version for major release"),
        ("minor", "m", "increment version for minor release"),
    ]

    boolean_options = ("major", "minor")

    def initialize_options(self):
        self.major = False
        self.minor = False

    def _new_version(self, version):
        major, minor, patch = [int(i) for i in version.split(".")]

        if self.major:
            return "{}.0.0".format(major + 1)
        elif self.minor:
            return "{}.{}.0".format(major, minor + 1)
        else:
            return "{}.{}.{}".format(major, minor, patch + 1)

    def _update_version(self):
        pattern = re.compile('^(\s+)version="([0-9\.]+)"')
        output = BytesIO()

        with open("setup.py", "r") as fp:
            for line in fp:
                result = pattern.match(line)

                if not result:
                    output.write(line)
                else:
                    spaces, version = result.groups()
                    new_version = self._new_version(version)
                    output.write(
                            '{}version="{}",\n'.format(spaces, new_version))

        with open("setup.py", "w") as fp:
            fp.write(output.getvalue())

        return new_version

    def _run(self):
        if simple_call("git status --porcelain").strip():
            raise DistutilsError("Uncommited changes, "
                                 "commit all changes before release")

        new_version = self._update_version()

        check_output([
            "git", "commit", "-m", "Release {}".format(new_version)])

        simple_call("git tag release-{}".format(new_version))


class GitPush(SimpleCommand):
    """Push changes and tags to git origin
    """

    description = "push changes to git origin"

    def _run(self):
        simple_call("git push origin master")
        simple_call("git push --tags")


class TestsWithCoverage(SimpleCommand):
    """Run Unit Tests with Coverage
    """

    description = "run unit tests with coverage"

    def _run(self):
        from coverage import coverage

        cov = coverage(data_file=".coverage", branch=True,
                       source=self.distribution.packages)
        cov.start()

        # Unittest calls exit. How naughty.
        try:
            self.run_command("test")
        except SystemExit:
            pass

        cov.stop()
        cov.xml_report(outfile="coverage.xml")
        cov.html_report()


class PEP8CheckStyle(SimpleCommand):
    """Run PEP8 Code Style Valiation
    """

    description = "run PEP8 style validations"

    def _run(self):
        from pep8 import StyleGuide

        self.run_command("egg_info")
        files = self.get_finalized_command("egg_info")

        report = StyleGuide().check_files([
            p for p in files.filelist.files if p.endswith(".py")])

        if report.total_errors:
            raise DistutilsError(
                    "Found {} PEP8 violations".format(report.total_errors))
        else:
            log.info("No PEP8 violations found")
