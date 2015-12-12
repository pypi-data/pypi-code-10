from seeker import ParamSeeker

seeker = ParamSeeker()

# add usage
seeker.set_usage_desc("seeker [OPTION]... ")
seeker.set_usage_desc('seeker thing')

seeker.set_desc("this is like a demo to tell how to use this package\n" +
                "also, this is my test project, with the name of seek\n" +
                "which is sick to see the source code, but the code is\n" +
                "at your source code dir, and you can visit\n\n" +
                "https://github.com/hellflame/paramSeeker/blob/master/seeker/example.py")


@seeker.seek('--linux', short='-l', extra={'desc': 'this is a test function', 'single_param': True})
def first(wanted):
    result = '\nthis is the first test method and it has got the argument \n\t`\033[01;31m{}\033[00m`\n'.\
        format(wanted)
    return result


@seeker.seek('--black', short='-b', extra={'desc': 'this is a test function'})
def second(wanted):
    result = '\nthis is the second test method and it has got the argument \n\t`\033[01;33m{}\033[00m`\n'.\
        format(wanted)
    return result


@seeker.seek()
def final(wanted):
    result = "Well ~~~ you got `\033[01;31m{}\033[00m`".format(wanted)
    return result


def test_env():
    seeker.run()

if __name__ == '__main__':
    seeker.run()

