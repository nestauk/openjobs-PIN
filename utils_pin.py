# import modules
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import matplotlib.patches as mpatches
import numpy as np


def print_elapsed(t0,task):
    print('Time spent on {} is {:.3f}s'.format(task,time.time()-t0))


def setup_tapi_url(MY_KEY = True, nb_of_calls = 0, max_calls = 98,
    dep_date = '2019-06-20', dep_time = '07:30', mode ='public'):
    key_file = '/Users/stefgarasto/Local-Data/sensitive-data/misc_keys.csv'
    keys = pd.read_csv(key_file)
    app_key = keys[keys['Key name']=='transport_api_my_key']['Key value']
    app_id = keys[keys['Key name']=='transport_api_my_id']['Key value']
    app_key_jyl = keys[keys['Key name']=='transport_api_jyl_key']['Key value']
    app_id_jyl = keys[keys['Key name']=='transport_api_jyl_id']['Key value']
    lon_from= '{}'
    lat_from = '{}'
    lon_to = '{}'
    lat_to = '{}'
    # this is the base urlname to call
    urlname_var = 'https://transportapi.com/v3/uk/{}'.format(mode) + '/journey/from/lonlat:{:5f},{:5f}/to/lonlat:{:5f},{:5f}'
    if MY_KEY:
        if mode == 'public':
            urlname_fix = '/at/{}/{}.json?app_id={}&app_key={}'.format(
            dep_date,dep_time,app_id,app_key)
        else:
            urlname_fix = '.json?app_id={}&app_key={}'.format(
            app_id,app_key)
    else:
        if mode == 'public':
            urlname_fix = '/at/{}/{}.json?app_id={}&app_key={}'.format(
            dep_date,dep_time,app_id_jyl,app_key_jyl)
        else:
            urlname_fix = '.json?app_id={}&app_key={}'.format(
            app_id_jyl,app_key_jyl)

    #print(urlname_var + urlname_fix)
    return urlname_fix, urlname_var


# set up Nesta colours
nesta_colours= [[1, 184/255, 25/255],[1,0,65/255],[0,0,0],
    [1, 90/255,0],[155/255,0,195/255],[165/255, 148/255, 130/255],
[160/255,145/255,40/255],[196/255,176/255,0],
    [246/255,126/255,0],[200/255,40/255,146/255],[60/255,18/255,82/255]]

# roughly, the colours are, in order:
# yellow , pink, black, orange, violet, grey, darkish green,
# light-ish grey, lighter orange, purple, kinda blue
# combos, the lists are for:
# primaries, secondaries, bright combination, warm combination
# cool combination, neutral with accent colour combination,
# deep and accent colour combination
nesta_colours_combos = [[0,1,2,3,4,5],[0,6,7],[1,3,8],
                [4,9,10],[8,5],[1,11]]


def modify_legend(l = None, **kwargs):
    import matplotlib as mpl

    if not l:
        l = plt.gca().legend_

    defaults = dict(
        loc = l._loc,
        numpoints = l.numpoints,
        markerscale = l.markerscale,
        scatterpoints = l.scatterpoints,
        scatteryoffsets = l._scatteryoffsets,
        prop = l.prop,
        # fontsize = None,
        borderpad = l.borderpad,
        labelspacing = l.labelspacing,
        handlelength = l.handlelength,
        handleheight = l.handleheight,
        handletextpad = l.handletextpad,
        borderaxespad = l.borderaxespad,
        columnspacing = l.columnspacing,
        ncol = l._ncol,
        mode = l._mode,
        fancybox = type(l.legendPatch.get_boxstyle())==mpl.patches.BoxStyle.Round,
        shadow = l.shadow,
        title = l.get_title().get_text() if l._legend_title_box.get_visible() else None,
        framealpha = l.get_frame().get_alpha(),
        bbox_to_anchor = l.get_bbox_to_anchor()._bbox,
        bbox_transform = l.get_bbox_to_anchor()._transform,
        frameon = l._drawFrame,
        handler_map = l._custom_handler_map,
    )

    if "fontsize" in kwargs and "prop" not in kwargs:
        defaults["prop"].set_size(kwargs["fontsize"])
    d = dict(defaults.items())
    d.update(kwargs.items())
    plt.legend(d) #**dict(defaults.items() + kwargs.items()))
