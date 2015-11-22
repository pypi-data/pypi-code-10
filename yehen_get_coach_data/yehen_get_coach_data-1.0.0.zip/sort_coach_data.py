#替换数据中的“-”和“：”为“.”
def sanitize(time_string):
    if time_string.find("-"):
        time_string=time_string.replace("-",".")
    if time_string.find("-"):
        time_string=time_string.replace(":",".")
    return time_string

#获取教练的记录，并返回字典格式的数据
def get_coach_data(file_name):
    dic={}
    try:
        with open(file_name) as file_out:
            results=file_out.readline().strip().split(",")
            dic["Name"]=results.pop(0)
            dic["DOB"]=results.pop(0)
            result_list=sorted(set([float(sanitize(item)) for item in results]))
            dic["Time"]=result_list
    except IOError as err:
        print("error info:"+str(err))
        return (None)
    return dic


#打印教练的记录
def print_coach_data(file_name):
    try:
        """with open(file_name) as file_out:
            results=file_out.readline()
            result_list=results.strip().split(",")
            result_list=[float(sanitize(each_t)) for each_t in result_list]
            print(sorted(set(result_list))[0:3])  
            print(set(result_list))"""
        dic=get_coach_data(file_name)
        print(dic['Name']+"'s fastest times are: "+
              str(dic['Time'][0:3]))
    except IOError as err:
        print("error Info:"+str(err))
            

	    
