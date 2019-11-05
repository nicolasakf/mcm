# -*- coding: utf-8 -*-
"""
Statistical methods for MCM data process
"""
import pandas as pd
import datetime as dt
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import os, shutil
from time import sleep

RELPATH = './app/static/res/figures'


def _format_df(df):
    out = df.dropna(how='all')
    out.rename(columns={'date': 'datetime'}, inplace=True)
    out['date'] = pd.DatetimeIndex(out['datetime']).date
    out = out.sort_values('datetime').reset_index(drop=True)
    out['elapsed'] = (out['datetime'] - out['datetime'][0]).dt.total_seconds()
    return out


def timebar_enumerate(df, tag_list):
    df = _format_df(df)
    df = df[tag_list+['elapsed', 'date']].set_index('date')
    df.index = pd.to_datetime(df.index)
    dates = df.index.drop_duplicates()
    status = {t: df[t].drop_duplicates().values for t in tag_list}

    out = {t: pd.DataFrame(index=dates, columns=status[t]) for t in tag_list}
    for t in tag_list:
        for d in dates:
            for s in status[t]:
                frame = df.loc[[d], [t, 'elapsed']]
                frame = frame[frame[t] == s]
                frame['elapsed_diff'] = frame['elapsed'].diff()
                frame = frame[frame['elapsed_diff'] < 10]
                if not frame.empty:  out[t].loc[d, s] = frame['elapsed_diff'].sum()
                else:  out[t].loc[d, s] = np.nan

    return out


# def compound(df_dict):
#     out = {k: pd.Series(index=v.columns) for k, v in df_dict}
#     for tag, df in df_dict.items():
#
#
#     return out


def plot_timeline(df_dict):
    out = {}
    for tag, df in df_dict.items():
        fig, ax = plt.subplots()
        ax.set_title(tag)

        df.index = df.index.date
        df.columns = df.columns.str.replace(' ', '')
        df = df.dropna(how='all').dropna(how='all', axis=1)
        df.plot.barh(ax=ax, align='center', stacked=True)
        ax.set_xlabel('Seconds Elapsed', fontsize=12)
        ax.set_ylabel('Date', fontsize=12)
        out[tag] = fig
        plt.close()

    return out


def export_figures(figs):
    out = {}
    shutil.rmtree(RELPATH)
    os.mkdir(RELPATH)
    for ft, f in figs.items():
        filepath = '{}/{}'.format(RELPATH, dt.datetime.now()).replace('.', 'd').replace(':', '').replace(' ', '_') + '.png'
        f.savefig(filepath)
        out[ft] = filepath[3:]

    return out


# df = pd.read_excel('/Users/NicolasFonteyne/GoogleDrive/Insper/10º semestre/2019-10-31 04_19_07.708884 016-020207-456.xlsx')
# res = timebar_enumerate(df, ['alm_list_msg1', 'alm_list_msg2', 'alm_list_msg3'])
# res = timebar_enumerate(df, ['pmc_alm1', 'pmc_alm2', 'pmc_alm3', 'pmc_alm4'])
# res = timebar_enumerate(df, ['auto_stat', 'edit_stat', 'emg_stat'])
# plots = plot_timeline(res)
