# -*- coding: utf-8 -*-
#
# This file is part of jsonresolver
# Copyright (C) 2015 CERN.
#
# jsonresolver is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

import jsonresolver


@jsonresolver.route('/test', host='http://localhost:4000')
def simple():
    return {'test': 'test'}
