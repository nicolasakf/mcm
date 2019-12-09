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
from app.core.utils import h, dhm

ROOTPATH = '/home/ubuntu/romi_legacy_new/app/static/res/figures'
# ROOTPATH = 'app/static/res/figures'


def _format_df(df):
    out = df.dropna(how='all')
    out.rename(columns={'date': 'datetime'}, inplace=True)
    out['date'] = pd.DatetimeIndex(out['datetime']).date
    out = out.sort_values('datetime').reset_index(drop=True)
    out['elapsed'] = (out['datetime'] - out['datetime'][0]).dt.total_seconds()
    return out


def timebar_enumerate(df, tag_list):
    df = _format_df(df)
    df = df[tag_list + ['elapsed', 'date']].set_index('date')
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
                if not frame.empty:
                    out[t].loc[d, s] = frame['elapsed_diff'].sum()
                else:
                    out[t].loc[d, s] = np.nan

    return out


def compound(df_dict):
    out = {}
    for tag, df in df_dict.items():
        out[tag] = df.sum()
    return out


def prep_auto(df_dict):
    auto_stat = df_dict['auto_stat']
    prep = auto_stat.drop('MEMory', axis=1).sum().sum()
    auto = auto_stat.sum()['MEMory']
    s = pd.Series([prep, auto], index=['PREP', 'AUTO'])
    out = {'Preparation Time / Automatic Time': s}
    return out


def avail(df):
    _avail = df[['alm_stat', 'emg_stat', 'date']].copy()
    _avail['avail_stat'] = 'NOT AVAILABLE'
    _avail['avail_stat'] = _avail['avail_stat'].mask(
        ((_avail.alm_stat == '****') & (_avail.emg_stat == 'Not emergency')),
        'AVAILABLE')
    availability = timebar_enumerate(_avail, ['avail_stat'])
    out = compound(availability)
    return out


def time_cut(df):
    cut = df[['timer_op', 'timer_cut']]
    cut = cut.iloc[-1] - cut.iloc[0]
    out = {'Cutting Time / Operating Time': cut}
    return out


def format_val(value, series, val=None):
    pct = value / series.sum()
    days = value / 60 / 60 / 24 if val is None else val * pct / 60 / 60 / 24
    _dhm = dhm(dt.timedelta(days))
    return '{}\n{:.2%}'.format(_dhm, pct)


def plot_compound(s_dict, value=None):
    out = {}
    for tag, s in s_dict.items():
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

        data = s.values
        strs = list(s.apply(lambda val: format_val(val, s, value)))

        wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40)

        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"),
                  bbox=bbox_props, zorder=0, va="center")

        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1) / 2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate(strs[i], xy=(x, y), xytext=(1.35 * np.sign(x), 1.4 * y),
                        horizontalalignment=horizontalalignment, **kw)
        ax.legend(s.index, loc='upper center', bbox_to_anchor=(0.5, -.125), ncol=1)
        ax.text(0.5, 1.2, tag,
                 horizontalalignment='center',
                 transform=ax.transAxes)
        out[tag + '_comp'] = fig
        plt.close()

    return out


def format_xaxis(value, _):
    days = value / 60 / 60 / 24
    return h(dt.timedelta(days))


def plot_timeline(df_dict):
    out = {}
    for tag, df in df_dict.items():
        fig, ax = plt.subplots()
        df.index = df.index.date
        df.columns = df.columns.str.replace(' ', '')
        df = df.dropna(how='all').dropna(how='all', axis=1)
        df.plot.barh(ax=ax, align='center', stacked=True)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(format_xaxis))
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -.125), ncol=1)
        ax.set_title(tag)
        out[tag] = fig
        plt.close()

    return out


def export_figures(figs, clear=True):
    out = {}
    if clear:
        try:
            shutil.rmtree(ROOTPATH)
            os.mkdir(ROOTPATH)
        except OSError:
            pass
    for ft, f in figs.items():
        filepath = ROOTPATH + '/' + str(dt.datetime.now()).replace('.', 'd').replace(':', '').replace(' ', '_') + '.png'
        f.savefig(filepath, bbox_inches='tight')
        out[ft] = filepath[32:]
        # out[ft] = filepath[3:]

    return out
