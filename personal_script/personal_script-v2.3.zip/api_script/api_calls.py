__author__ = 'seshadribt24'
import requests
from json_parser_insights import JsonParser
import csv
import time
import datetime
from multiprocessing import Pool


class ApiFiltered(object):
    def __init__(self, token='', ad_account='', campaign_id='', adset_id='', adgroup_id='', start='', end='', save=True,
                 save_location=''):
        self.token = token.strip()
        self.ad_account = ad_account.strip()
        self.campaign_id = campaign_id.strip()
        self.adset_id = adset_id.strip()
        self.adgroup_id = adgroup_id.strip()
        self.start = start.strip()
        self.end = end.strip()
        self.save = save
        self.save_location = save_location

    def filtered_call(self, static=False, end_date=''):
        # url parameters
        if self.campaign_id != '':
            filter_string = '['
            for campaign_id in self.campaign_id.split(","):
                filter_string += '"' + str(campaign_id) + '",'
            filter_string = filter_string[:-1] + "]"
            filter_campaign_id = ',{"field":"campaign_group.id","operator":"IN","value":' + filter_string + '}'
            level = '&level=campaign'
        else:
            filter_campaign_id = ''

        fields = '&fields=["campaign_name","campaign_group_id","campaign_delivery","results","performance_indicator",' \
                 '"reach","cost_per_result","campaign_budget_value","campaign_budget_type","spend",' \
                 '"campaign_end","campaign_start"]'

        action_breakdown = "&default_summary=true"

        filtering = '&filtering=[{"field":"adgroup.delivery_info","operator":"IN","value":' \
                    '["active","archived","completed","inactive","not_delivering","not_published","pending_review",' \
                    '"recently_completed","recently_rejected","rejected","scheduled","permanently_deleted"]}' \
                    + filter_campaign_id + ']'

        export_columns = '&export_columns=["campaign_name", "campaign_group_id", "campaign_delivery", "results",' \
                         '"performance_indicator", "reach", "cost_per_result", "campaign_budget_value",' \
                         '"campaign_budget_type", "spend", "campaign_end", "campaign_start"]'

        action_list = 0

        non_action_list = ["date_start", "date_stop", "account_id", "spend",
                           "reach"]

        relevance_score = 0
        video_view_list = 0
        action_values = 0

        if static:
            time_range = '&time_range={"since": "' + self.start + '", "until": "' + end_date + '"}'
        else:
            time_range = '&time_range={"since": "' + self.start + '", "until": "' + self.end + '"}'

        # url
        url = 'https://graph.facebook.com/v2.3/act_' + self.ad_account + '/insights?' \
                                                                         'access_token=' + self.token + \
              '&action_attribution_windows=["default"]' \
              + fields + filtering + action_breakdown + level + time_range + export_columns + '&method=post'
        print url

        # post url
        report_run_id = requests.post(url)
        try:
            report_id = report_run_id.json()['report_run_id']
        except:
            print report_run_id.text

        # get job status
        url = 'https://graph.facebook.com/v2.4/' + report_id + '?access_token=' + self.token
        print "report run url is: ", url
        run = True
        while run is True:
            time.sleep(2)
            response = requests.get(url)
            status = response.json()['async_status']
            print status
            if 'Completed' in status:
                run = False
            elif 'Failed' in status:
                exit()
                break
            else:
                continue

        # get data
        data = JsonParser(report_id, self.token, fields, self.ad_account, action_list, video_view_list,
                          non_action_list, action_values, relevance_score)
        parser = data.parser_summary_row()

        if self.save:
            with open(str(self.save_location) + 'data_' + str(self.ad_account.strip()) + '.csv',
                      'wb+') as g:
                s = csv.writer(g)
                s.writerow(["Start Date",
                            "End Date",
                            "Account ID",
                            "Spend",
                            "Reach"])
                for row in parser:
                    for data in row:
                        s.writerow(data)
        else:
            return parser

    @staticmethod
    def date_generator(start, num_of_days):
        for num in range(int(num_of_days)):
            yield (start + datetime.timedelta(days=num)).strftime("%Y-%m-%d")

    def incremental_reach(self):
        # finding the number of days
        start_changed = datetime.datetime.strptime(self.start, "%Y-%m-%d")
        end_changed = datetime.datetime.strptime(self.end, "%Y-%m-%d")
        num_of_days = int((end_changed - start_changed).days)

        # declaring variable that'll hold the data returned from api
        master_data = []

        # generating the calls
        dates = self.date_generator(start_changed, num_of_days)
        for generator_end_date in dates:
            # print generator_end_date
            call = self.filtered_call(static=True, end_date=generator_end_date)
            master_data.append(call)

        return master_data

    def only_ids(self):
        if self.adgroup_id != '':
            # parameters
            ids_array = self.adgroup_id.split(",")
            columns = '["campaign_group_name", "campaign_group_id", "campaign_name", "campaign_id", "adgroup_name",' \
                      '"adgroup_id", "relevance_score"]'
            non_action_items = ["campaign_group_name", "campaign_group_id", "campaign_name", "campaign_id",
                                "adgroup_name",
                                "adgroup_id"]
            relevance_score = ['score']

            data = JsonParser(export_columns=columns, token=self.token, non_action_list=non_action_items,
                              relevance_score=relevance_score)

            data_array = []
            for ids in ids_array:
                parser = data.parser_ids(ids, self.start, self.end)
                data_array.append(parser)

            if self.save:
                with open(str(self.save_location) + 'data_relevance_score.csv',
                          'wb+') as g:
                    s = csv.writer(g)
                    s.writerow(["campaign_group_name",
                                "campaign_group_id",
                                "campaign_name",
                                "campaign_id",
                                "adgroup_name",
                                "adgroup_id",
                                "relevance_score"])
                    for row in data_array:
                        s.writerow(row)
            else:
                return data_array
        elif self.campaign_id != '':
            # parameters
            ids_array = self.campaign_id.split(",")
            columns = '["account_name","account_id","campaign_group_name","campaign_group_id","reach","frequency",' \
                      '"impressions","spend","cpm","cpp","cost_per_total_action","actions",' \
                      '"video_avg_sec_watched_actions","video_avg_pct_watched_actions","video_p100_watched_actions",' \
                      '"cost_per_action_type","video_10_sec_watched_actions","cost_per_10_sec_video_view",' \
                      '"video_complete_watched_actions","cpc","ctr"]'
            non_action_items = ["account_name", "account_id", "campaign_group_name", "campaign_group_id", "reach", "frequency",
                                "impressions", "spend", "cpm", "cpp", "cpc", "ctr"]
            relevance_score = 0
            action_list = ["app_custom_event.fb_mobile_activate_app", "app_custom_event.fb_mobile_add_to_cart",
                           "app_custom_event.fb_mobile_add_to_wishlist", "mobile_app_install", "post_like",
                           "page_engagement", "post_engagement", "app_custom_event"]

            data = JsonParser(export_columns=columns, token=self.token, non_action_list=non_action_items,
                              relevance_score=relevance_score, action_list=action_list)

            data_array = []
            for ids in ids_array:
                parser = data.parser_campaign_ids(ids, self.start, self.end)
                data_array.append(parser)

            if self.save:
                with open(str(self.save_location) + 'data_relevance_score.csv',
                          'wb+') as g:
                    s = csv.writer(g)
                    s.writerow(["account_name", "account_id", "campaign_group_name", "campaign_group_id", "reach",
                                "frequency",
                                "impressions", "spend", "cpm", "cpp", "cpc", "ctr",
                                "app_custom_event.fb_mobile_activate_app", "app_custom_event.fb_mobile_add_to_cart",
                                "app_custom_event.fb_mobile_add_to_wishlist", "mobile_app_install", "post_like",
                                "page_engagement", "post_engagement", "app_custom_event"])
                    for lines in data_array:
                        for row in lines:
                            s.writerow(row)
            else:
                return data_array
