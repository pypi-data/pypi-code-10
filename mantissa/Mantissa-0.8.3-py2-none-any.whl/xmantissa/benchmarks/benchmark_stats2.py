import datetime
from axiom import store
from xmantissa import stats, webadmin
from epsilon import extime
from epsilon.scripts import benchmark

def main():
    s = store.Store("stats.axiom")
    sampler = stats.StatSampler(store=s)
    t = extime.Time()
    svc = stats.StatsService(store=s, currentMinuteBucket=100)
    for x in range(100):

        scope = stats.Statoscope("")
        scope._stuffs = {'bandwidth_http_down': 0, 'bandwidth_pop3_up': 0, 'bandwidth_sip_up': 0, 'Imaginary logins': 0, 'bandwidth_pop3-grabber_down': 0, 'SMTP logins': 0, 'actionExecuted': 0, 'bandwidth_pop3_down': 0, 'bandwidth_ssh_up': 0, 'cursor_execute_time': 0.15660834312438965, 'actionDuration': 0, 'bandwidth_smtps_up': 0, 'messages_grabbed': 0, 'bandwidth_smtps_down': 0, 'athena_messages_sent': 0, 'page_renders': 0, 'autocommits': 0, 'cache_hits': 7, 'bandwidth_telnet_up': 0, 'bandwidth_smtp_up': 0, 'bandwidth_sip_down': 0, 'bandwidth_http_up': 0, 'commits': 9, 'messagesSent': 0, 'bandwidth_ssh_down': 0, 'athena_messages_received': 0, 'bandwidth_https_up': 0, 'bandwidth_https_down': 0, 'cache_misses': 9, 'bandwidth_pop3s_down': 0, 'POP3 logins': 0, 'cursor_blocked_time': 0.0, 'messagesReceived': 0, 'bandwidth_telnet_down': 0, 'bandwidth_smtp_down': 0, 'mimePartsCreated': 0, 'bandwidth_pop3-grabber_up': 0, 'Web logins': 0, 'bandwidth_pop3s_up': 0}
        queryscope = stats.Statoscope("")
        queryscope._stuffs = {u'_axiom_query:SELECT main.item_axiom_batch__reliablelistener_v1.oid, main.item_axiom_batch__reliablelistener_v1.[backwardMark], main.item_axiom_batch__reliablelistener_v1.[forwardMark], main.item_axiom_batch__reliablelistener_v1.[lastRun], main.item_axiom_batch__reliablelistener_v1.[listener], main.item_axiom_batch__reliablelistener_v1.[processor], main.item_axiom_batch__reliablelistener_v1.[style] FROM main.item_axiom_batch__reliablelistener_v1 WHERE ((main.item_axiom_batch__reliablelistener_v1.[processor] = ?) AND (main.item_axiom_batch__reliablelistener_v1.[style] = ?) AND main.item_axiom_batch__reliablelistener_v1.[listener] NOT IN ()) ORDER BY main.item_axiom_batch__reliablelistener_v1.[lastRun] ASC ': 0, u'_axiom_query:SELECT main.item_xquotient_grabber_pop3uid_v1.[value] FROM main.item_xquotient_grabber_pop3uid_v1 WHERE (main.item_xquotient_grabber_pop3uid_v1.[grabberID] = ?)  ': 0, u'_axiom_query:SELECT main.item_axiom_powerup_connector_v1.oid, main.item_axiom_powerup_connector_v1.[interface], main.item_axiom_powerup_connector_v1.[item], main.item_axiom_powerup_connector_v1.[powerup], main.item_axiom_powerup_connector_v1.[priority] FROM main.item_axiom_powerup_connector_v1 WHERE ((main.item_axiom_powerup_connector_v1.[interface] = ?) AND (main.item_axiom_powerup_connector_v1.[item] = ?)) ORDER BY main.item_axiom_powerup_connector_v1.[priority] DESC ': 0, u'_axiom_query:SELECT main.item_xmantissa_stats_statsservice_v1.oid, main.item_xmantissa_stats_statsservice_v1.[currentMinuteBucket], main.item_xmantissa_stats_statsservice_v1.[currentQuarterHourBucket], main.item_xmantissa_stats_statsservice_v1.[installedOn] FROM main.item_xmantissa_stats_statsservice_v1   LIMIT 2': 0, u'_axiom_query:SELECT main.item_login_v2.oid, main.item_login_v2.[avatars], main.item_login_v2.[disabled], main.item_login_v2.[password] FROM main.item_login_v2, main.item_login_method_v2 WHERE ((main.item_login_method_v2.[domain] = ?) AND (main.item_login_method_v2.[localpart] = ?) AND (main.item_login_v2.[disabled] = ?) AND (main.item_login_method_v2.[account] = main.item_login_v2.oid))  ': 0, u'_axiom_query:SELECT main.item_login_method_v2.oid, main.item_login_method_v2.[account], main.item_login_method_v2.[domain], main.item_login_method_v2.[internal], main.item_login_method_v2.[localpart], main.item_login_method_v2.[protocol], main.item_login_method_v2.[verified] FROM main.item_login_method_v2   ': 0, u'_axiom_query:SELECT main.item_timed_event_v1.oid, main.item_timed_event_v1.[runnable], main.item_timed_event_v1.[time] FROM main.item_timed_event_v1 WHERE (main.item_timed_event_v1.[time] < ?) ORDER BY main.item_timed_event_v1.[time] ASC LIMIT 1': 0, u'_axiom_query:SELECT main.item_login_v2.oid, main.item_login_v2.[avatars], main.item_login_v2.[disabled], main.item_login_v2.[password] FROM main.item_login_v2   ': 0, u'_axiom_query:SELECT main.item_xmantissa_stats_statbucket_v1.oid, main.item_xmantissa_stats_statbucket_v1.[index], main.item_xmantissa_stats_statbucket_v1.[interval], main.item_xmantissa_stats_statbucket_v1.[time], main.item_xmantissa_stats_statbucket_v1.[type], main.item_xmantissa_stats_statbucket_v1.[value] FROM main.item_xmantissa_stats_statbucket_v1 WHERE ((main.item_xmantissa_stats_statbucket_v1.[type] = ?) AND (main.item_xmantissa_stats_statbucket_v1.[interval] = ?) AND ((main.item_xmantissa_stats_statbucket_v1.[index] >= ?) OR (main.item_xmantissa_stats_statbucket_v1.[index] <= ?)))  ': 0, u'_axiom_query:SELECT main.item_timed_event_v1.oid, main.item_timed_event_v1.[runnable], main.item_timed_event_v1.[time] FROM main.item_timed_event_v1  ORDER BY main.item_timed_event_v1.[time] ASC LIMIT 1': 0, u'_axiom_query:SELECT main.item_persistent_session_v1.oid, main.item_persistent_session_v1.[authenticatedAs], main.item_persistent_session_v1.[lastUsed], main.item_persistent_session_v1.[sessionKey] FROM main.item_persistent_session_v1 WHERE (main.item_persistent_session_v1.[sessionKey] = ?)  ': 0, u'_axiom_query:SELECT main.item_login_v2.oid, main.item_login_v2.[avatars], main.item_login_v2.[disabled], main.item_login_v2.[password] FROM main.item_login_v2 WHERE (main.item_login_v2.[disabled] != ?)  ': 0, u'_axiom_query:SELECT main.item_login_v2.oid, main.item_login_v2.[avatars], main.item_login_v2.[disabled], main.item_login_v2.[password] FROM main.item_login_v2, main.item_login_method_v2 WHERE ((main.item_login_method_v2.[domain] IS NULL) AND (main.item_login_method_v2.[localpart] = ?) AND (main.item_login_v2.[disabled] = ?) AND (main.item_login_method_v2.[account] = main.item_login_v2.oid))  ': 0, u'_axiom_query:SELECT main.item_mantissa_installed_offering_v1.oid, main.item_mantissa_installed_offering_v1.[application], main.item_mantissa_installed_offering_v1.[offeringName] FROM main.item_mantissa_installed_offering_v1 WHERE (main.item_mantissa_installed_offering_v1.[offeringName] = ?)  LIMIT 1': 0, u'_axiom_query:SELECT main.item_imaginary_wiring_realm_playercredentials_v1.oid, main.item_imaginary_wiring_realm_playercredentials_v1.[actor], main.item_imaginary_wiring_realm_playercredentials_v1.[password], main.item_imaginary_wiring_realm_playercredentials_v1.[username] FROM main.item_imaginary_wiring_realm_playercredentials_v1 WHERE (main.item_imaginary_wiring_realm_playercredentials_v1.[actor] = ?)  ': 0, u'_axiom_query:SELECT main.item_login_system_v1.oid, main.item_login_system_v1.[failedLogins], main.item_login_system_v1.[loginCount] FROM main.item_login_system_v1   ': 0, '_axiom_query:SELECT main.item_xmantissa_stats_statbucket_v1.oid, main.item_xmantissa_stats_statbucket_v1.[index], main.item_xmantissa_stats_statbucket_v1.[interval], main.item_xmantissa_stats_statbucket_v1.[time], main.item_xmantissa_stats_statbucket_v1.[type], main.item_xmantissa_stats_statbucket_v1.[value] FROM main.item_xmantissa_stats_statbucket_v1 WHERE ((main.item_xmantissa_stats_statbucket_v1.[interval] = ?) AND (main.item_xmantissa_stats_statbucket_v1.[type] = ?) AND (main.item_xmantissa_stats_statbucket_v1.[time] = ?))  ': 0, '_axiom_query:SELECT main.item_xmantissa_stats_statbucket_v1.oid, main.item_xmantissa_stats_statbucket_v1.[index], main.item_xmantissa_stats_statbucket_v1.[interval], main.item_xmantissa_stats_statbucket_v1.[time], main.item_xmantissa_stats_statbucket_v1.[type], main.item_xmantissa_stats_statbucket_v1.[value] FROM main.item_xmantissa_stats_statbucket_v1 WHERE ((main.item_xmantissa_stats_statbucket_v1.[interval] = ?) AND (main.item_xmantissa_stats_statbucket_v1.[type] = ?) AND (main.item_xmantissa_stats_statbucket_v1.[time] = ?))  ': 0, '_axiom_query:SELECT main.item_xmantissa_stats_statbucket_v1.oid, main.item_xmantissa_stats_statbucket_v1.[index], main.item_xmantissa_stats_statbucket_v1.[interval], main.item_xmantissa_stats_statbucket_v1.[time], main.item_xmantissa_stats_statbucket_v1.[type], main.item_xmantissa_stats_statbucket_v1.[value] FROM main.item_xmantissa_stats_statbucket_v1 WHERE ((main.item_xmantissa_stats_statbucket_v1.[index] = ?) AND (main.item_xmantissa_stats_statbucket_v1.[interval] = ?))  ': 0, u'_axiom_query:SELECT main.item_imaginary_objects_exit_v1.oid, main.item_imaginary_objects_exit_v1.[fromLocation], main.item_imaginary_objects_exit_v1.[name], main.item_imaginary_objects_exit_v1.[sibling], main.item_imaginary_objects_exit_v1.[toLocation] FROM main.item_imaginary_objects_exit_v1 WHERE (main.item_imaginary_objects_exit_v1.[toLocation] = ?)  ': 0, u'_axiom_query:SELECT main.item_mantissa_installed_offering_v1.[offeringName] FROM main.item_mantissa_installed_offering_v1   ': 0, u'_axiom_query:SELECT main.item_imaginary_objects_exit_v1.oid, main.item_imaginary_objects_exit_v1.[fromLocation], main.item_imaginary_objects_exit_v1.[name], main.item_imaginary_objects_exit_v1.[sibling], main.item_imaginary_objects_exit_v1.[toLocation] FROM main.item_imaginary_objects_exit_v1 WHERE (main.item_imaginary_objects_exit_v1.[fromLocation] = ?)  ': 0, u'_axiom_query:SELECT main.item_axiom_subscheduler_parent_hook_v1.oid, main.item_axiom_subscheduler_parent_hook_v1 main.item_xmantissa_search_searchresult_v1.[identifier], main.item_xmantissa_search_searchresult_v1.[indexedItem] FROM main.item_xmantissa_search_searchresult_v1 WHERE (main.item_xmantissa_search_searchresult_v1.[indexedItem] = ?)  ': 0, '_axiom_query:SELECT main.item_xmantissa_stats_statbucket_v1.oid, main.item_xmantissa_stats_statbucket_v1.[index], main.item_xmantissa_stats_statbucket_v1.[interval], main.item_xmantissa_stats_statbucket_v1.[time], main.item_xmantissa_stats_statbucket_v1.[type], main.item_xmantissa_stats_statbucket_v1.[value] FROM main.item_xmantissa_stats_statbucket_v1 WHERE ((main.item_xmantissa_stats_statbucket_v1.[index] = ?) AND (main.item_xmantissa_stats_statbucket_v1.[interval] = ?) AND (main.item_xmantissa_stats_statbucket_v1.[type] = ?))  ': 0, u'_axiom_query:SELECT main.item_developer_site_v1.oid, main.item_developer_site_v1.[administrators], main.item_developer_site_v1.[developers] FROM main.item_developer_site_v1   ': 0}
        sampler.service = svc
        sampler.doStatSample(s, scope, t, [])
        sampler.doStatSample(s, queryscope, t, [], bucketType=stats.QueryStatBucket)
        t = t + datetime.timedelta(minutes=1)

    asf = webadmin.AdminStatsFragment()
    asf._initializeObserver = lambda : None
    asf.svc = svc
    benchmark.start()
    asf.buildPie()
    benchmark.stop()
    
if __name__ == '__main__':
    main()
