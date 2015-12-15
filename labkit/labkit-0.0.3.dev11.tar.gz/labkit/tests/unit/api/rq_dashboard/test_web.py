#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import unittest

from labkit.api.rq_dashboard import web

class TestWeb(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_setup_rq_connection(self):
        return
        web.setup_rq_connection()


    def test_push_rq_connection(self):
        return
        web.push_rq_connection()


    def test_pop_rq_connection(self):
        return
        web.pop_rq_connection(exception=None)


    def test_jsonify(self):
        return
        web.jsonify(f)


    def test__wrapped(self):
        return
        web._wrapped(*args, **kwargs)


    def test_serialize_queues(self):
        return
        web.serialize_queues(queues)


    def test_serialize_date(self):
        return
        web.serialize_date(dt)


    def test_serialize_job(self):
        return
        web.serialize_job(job)


    def test_remove_none_values(self):
        return
        web.remove_none_values(input_dict)


    def test_pagination_window(self):
        return
        web.pagination_window(total_items, cur_page, per_page=5, window_size=10)


    def test_overview(self):
        return
        web.overview(queue_name, page)


    def test_cancel_job_view(self):
        return
        web.cancel_job_view(job_id)


    def test_requeue_job_view(self):
        return
        web.requeue_job_view(job_id)


    def test_requeue_all(self):
        return
        web.requeue_all()


    def test_empty_queue(self):
        return
        web.empty_queue(queue_name)


    def test_compact_queue(self):
        return
        web.compact_queue(queue_name)


    def test_list_queues(self):
        return
        web.list_queues()


    def test_list_jobs(self):
        return
        web.list_jobs(queue_name, page)


    def test_list_workers(self):
        return
        web.list_workers()


    def test_serialize_queue_names(self):
        return
        web.serialize_queue_names(worker)


    def test_inject_interval(self):
        return
        web.inject_interval()



if __name__ == '__main__':
    unittest.main()



