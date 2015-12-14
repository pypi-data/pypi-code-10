import datetime
import cgi

from bson.objectid import ObjectId
from bson.code import Code

from helper_functions import *


class Application:

    def __init__(self, default_config):
        self.collection = default_config['APPLICATIONS_COLLECTION']
        self.response = {'error': None, 'data': None}
        self.debug_mode = default_config['DEBUG']

    def get_view(self,title="title",email="email"):

        mapper = Code("""
                      function () {
                         var key = this.%(title)s
                         var value = {
                         count :1,
                         %(email)s:
                         [{
                            count: 1,
                            %(email)s: this.%(email)s,
                            permalink:this.permalink,
                            id:this._id,
                            date:this.date,
                            status:this.status

                        }]
                        }
                        ;

                          emit(key, value);
                      }
                      """ % locals()  )
       # //emit(this."""+title+", {count:1,"+email+"+:[{"+email+":this."+email+""",permalink:this.permalink,id:this._id,date:this.date,status:this.status}]});

        reducer = Code("""
                       function (key, values) {
                         var total = 0;
                         var emails=new Array();
                        for (var i = 0; i < values.length; i++) {
                        total += values[i].count;
                        emails.push(values[i].%(email)s[0]);
                  }
                         return {count:total,%(email)s:emails};
                       }
                       """ % locals())

        reducer2 = Code("""
                               function (key, values) {

                                 return {count:1,"""+email+""":values};
                               }
                               """)


        result = self.collection.map_reduce(map=mapper, reduce=reducer, out="myresults")
        cursor= result.find()
        ans=[]
        for c in cursor:
            ans.append({title:c['_id'],'count':int(c['value']['count']),email:c['value'][email]})
        return ans

    # def get_title_email(self,arg,title="title",email="email"):
    #
    #     emails=self.collection.find(title=arg)
    #     emails.length
    #     mapper = Code("""
    #                   function () {
    #                       emit(this."""+title+", {count:1,"+email+":this."+email+""",permalink:this.permalink,id:this._id,date:this.date,applicant:this.applicant,status:this.status,applicant:this.applicant});
    #                   }
    #                   """)
    #
    #     reducer = Code("""
    #                    function (key, values) {
    #                      var total = 0;
    #                     for (var i = 0; i < values.length; i++) {
    #                 total += values[i].count;
    #                 applicant=values[i].applicant;
    #               }
    #                      return {count:total,"""+email+""":values,applicant:applicant};
    #                    }
    #                    """)
    #     result = self.collection.map_reduce(mapper, reducer, "myresults")
    #     cursor= result.find()
    #     ans=[]
    #     for c in cursor:
    #         # print c
    #         ans.append({title:c['_id'],'applicant':c['value']['applicant'],'count':int(c['value']['count']),email:c['value'][email]})
    #     print ans
    #     return ans







    def get_applications(self, limit, skip, tag=None, search=None):
        self.response['error'] = None
        cond = {}
        if tag is not None:
            cond = {'tags': tag}
        elif search is not None:
            cond = {'$or': [
                    {'title': {'$regex': search, '$options': 'i'}},
                    {'body': {'$regex': search, '$options': 'i'}},
                    {'preview': {'$regex': search, '$options': 'i'}}]}
        try:
            cursor = self.collection.find(cond).sort(
                'date', direction=-1).skip(skip).limit(limit)
            self.response['data'] = []
            for application in cursor:
                if 'tags' not in application:
                    application['tags'] = []
                if 'comments' not in application:
                    application['comments'] = []
                if 'preview' not in application:
                    application['preview'] = ''

                self.response['data'].append({'id': application['_id'],
                                              'title': application['title'],
                                              'body': application['body'],
                                              'preview': application['preview'],
                                              'date': application['date'],
                                              'applicant': application['applicant'],
                                              'status': application['status'],
                                              'email': application['email'],
                                              'permalink': application['permalink'],
                                              'molecule_link': application['molecule_link'],
                                              'tags': application['tags'],
                                              'author': application['author'],
                                              'comments': application['comments']})
        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Applications not found..'

        return self.response

    def get_application_by_permalink(self, permalink):
        self.response['error'] = None
        try:
            self.response['data'] = self.collection.find_one(
                {'permalink': permalink})
        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Application not found..'

        return self.response

    def get_application_by_id(self, application_id):
        self.response['error'] = None
        try:
            self.response['data'] = self.collection.find_one(
                {'_id': ObjectId(application_id)})
            if self.response['data']:
                if 'tags' not in self.response['data']:
                    self.response['data']['tags'] = ''
                else:
                    self.response['data']['tags'] = ','.join(
                        self.response['data']['tags'])
                if 'preview' not in self.response['data']:
                    self.response['data']['preview'] = ''
        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Application not found..'

        return self.response

    def get_total_count(self, tag=None, search=None):
        cond = {}
        if tag is not None:
            cond = {'tags': tag}
        elif search is not None:
            cond = {'$or': [
                    {'title': {'$regex': search, '$options': 'i'}},
                    {'body': {'$regex': search, '$options': 'i'}},
                    {'preview': {'$regex': search, '$options': 'i'}}]}

        return self.collection.find(cond).count()

    def get_tags(self):
        self.response['error'] = None
        try:
            self.response['data'] = self.collection.aggregate([
                {'$unwind': '$tags'},
                {'$group': {'_id': '$tags', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 10},
                {'$project': {'title': '$_id', 'count': 1, '_id': 0}}
            ])
            if self.response['data']['result']:
                self.response['data'] = self.response['data']['result']
            else:
                self.response['data'] = []

        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Get tags error..'

        return self.response

    def create_new_application(self, application_data):
        self.response['error'] = None
        try:
            self.response['data'] = self.collection.insert(application_data)
        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Adding application error..'

        return self.response

    def edit_application(self, application_id, application_data):
        self.response['error'] = None
        del application_data['date']
        del application_data['permalink']

        try:
            self.collection.update(
                {'_id': ObjectId(application_id)}, {"$set": application_data}, upsert=False)
            self.response['data'] = True
        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Application update error..'

        return self.response

    def delete_application(self, application_id):
        self.response['error'] = None
        try:
            if self.get_application_by_id(application_id) and self.collection.remove({'_id': ObjectId(application_id)}):
                self.response['data'] = True
            else:
                self.response['data'] = False
        except Exception, e:
            self.print_debug_info(e, self.debug_mode)
            self.response['error'] = 'Deleting application error..'

        return self.response

    @staticmethod
    def validate_application_data(application_data):
        permalink = random_string(12)
        #exp = re.compile('\W')
        #whitespace = re.compile('\s')
        #temp_title = whitespace.sub("_", application_data['title'])
        #permalink = exp.sub('', temp_title)

        application_data['title'] = cgi.escape(application_data['title'])
        # application_data['preview'] = cgi.escape(application_data['preview'], quote=True)
        application_data['body'] = cgi.escape(application_data['body'], quote=True)
        application_data['date'] = datetime.datetime.utcnow()
        application_data['permalink'] = permalink
        application_data['email'] = cgi.escape(application_data['email'])
        application_data['status'] = None

        return application_data

    @staticmethod
    def print_debug_info(msg, show=False):
        if show:
            import sys
            import os

            error_color = '\033[32m'
            error_end = '\033[0m'

            error = {'type': sys.exc_info()[0].__name__,
                     'file': os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename),
                     'line': sys.exc_info()[2].tb_lineno,
                     'details': str(msg)}

            print error_color
            print '\n\n---\nError type: %s in file: %s on line: %s\nError details: %s\n---\n\n'\
                  % (error['type'], error['file'], error['line'], error['details'])
            print error_end
