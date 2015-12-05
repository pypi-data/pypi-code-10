from xml.dom import minidom


def read_test_xml(file_name):
    return_list = []
    test_file = open(file_name, 'r')
    xmldoc = minidom.parse(test_file)
    test_file.close()
    testsuite = xmldoc.getElementsByTagName('testsuite')
    test_nr = testsuite[0].attributes['tests'].value
    error_nr = testsuite[0].attributes['errors'].value
    failure_nr = testsuite[0].attributes['failures'].value

    case_list = xmldoc.getElementsByTagName('testcase')
    total_time = 0
    for case in case_list:
        total_time += float(case.attributes['time'].value)

    return_list.append(test_nr)
    return_list.append(error_nr)
    return_list.append(failure_nr)
    return_list.append(unicode(total_time))
    print ("nr of tests : " + return_list[0])
    print ("nr of errors : " + return_list[1])
    print ("nr of failures : " + return_list[2])
    print ("total test time : " + return_list[3])

    # return return_list
if __name__ == "__main__":
    read_test_xml("test_output.xml")
