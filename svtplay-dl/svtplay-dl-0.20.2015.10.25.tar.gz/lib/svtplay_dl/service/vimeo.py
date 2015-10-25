# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
from __future__ import absolute_import
import json
import re
import copy

from svtplay_dl.service import Service, OpenGraphThumbMixin
from svtplay_dl.fetcher.http import HTTP
from svtplay_dl.error import ServiceError


class Vimeo(Service, OpenGraphThumbMixin):
    supported_domains = ['vimeo.com']

    def get(self, options):
        data = self.get_urldata()

        if self.exclude(options):
            yield ServiceError("Excluding video")
            return

        match = re.search('data-config-url="([^"]+)" data-fallback-url', data)
        if not match:
            yield ServiceError("Can't find video file for: %s" % self.url)
            return
        player_url = match.group(1).replace("&amp;", "&")
        player_data = self.http.request("get", player_url).text

        if player_data:
            jsondata = json.loads(player_data)
            avail_quality = jsondata["request"]["files"]["h264"]
            for i in avail_quality.keys():
                yield HTTP(copy.copy(options), avail_quality[i]["url"], avail_quality[i]["bitrate"])
        else:
            yield ServiceError("Can't find any streams.")
            return
