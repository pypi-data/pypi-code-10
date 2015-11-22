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
            dic["Times"]=result_list
    except IOError as err:
        print("error info:"+str(err))
        return (None)
    return dic

class Athlete:
    def __init__(self,a_name,a_dob=None,a_times=[]):
        self.name=a_name
        self.dob=a_dob
        self.times=a_times
    def top3(self):
        return sorted(set(self.times))[0:3]


#打印教练的记录
def print_coach_data(file_name):
    try:
        
        dic=get_coach_data(file_name)
        athlete=Athlete(dic['Name'],dic['DOB'],dic['Times'])
        print(athlete.name+"'s fastest times are: "+
              str(athlete.top3()))
    except IOError as err:
        print("error Info:"+str(err))
            

	    
