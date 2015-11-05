from __future__ import absolute_import
import getpass
from flask import Blueprint
from flask import render_template


bprint = Blueprint(u'gemon', __name__, template_folder=u'templates')


@bprint.route(u'/')
def home():
    import numpy as np
    from .ge import qstat
    import pandas as pd
    # df_user = qstat()
    df_all = qstat(u'*')
    if len(df_all) != 0:
        df_user = df_all[df_all[u'JB_owner'] == getpass.getuser()]


        def summarize(df):
            def f():
                for state, df_ in df.groupby([u'state']):
                    yield u'%s_jobs' % state, [len(df_)]
                    yield u'%s_slots' % state, [df_.slots.astype(int).sum()]

                yield u'sum(io_usage)', [u"{:,}".format(int(np.nan_to_num(df.io_usage.astype(float).sum())))]

            return pd.DataFrame(dict(f()))

        df_user_summary = summarize(df_user)
        df_all_summary = summarize(df_all)
    else:
        df_user_summary, df_all_summary = None, None

    return render_template(u'gemon/home.html', df_user=df_user, df_user_summary=df_user_summary,
                           df_all_summary=df_all_summary)