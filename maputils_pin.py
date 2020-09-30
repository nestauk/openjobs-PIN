# this file contains utility functions that can only be called when the
# mapping environment is active

# import modules
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import matplotlib.patches as mpatches
import numpy as np

# Geometry, shapefiles and projections
import fiona
from shapely.geometry import shape
from shapely.geometry import Point
import pyproj
from descartes import PolygonPatch
from shapely.ops import transform



def draw_map(data, col, color_scheme, data_min, data_max, gb_filename, ni_filename,
             shp_filename, subset_outlines = None,
             roi_col = 'TTWA code', shp_col = 'ttwa11cd', params = {'SAVEFIG': False},
             fig = None, ax = None):
    '''This function is used to plot a map of the LSOAs in a TTWA colour-coded
    based on variables of interest.
    It takes a dataframe (i.e. data) with the relevant values and a column
        with the TTWA codes (whose name can be passed as the ttwa_code argument),
        the column to plot, the colour scheme and the min and max.
     Other parameters:
     gb_filename: shape file with GB boundaries or whatever
     large region we want to plot
     ni_filename = shape file with NI boundaries
     shp_filename: shape file with boundaries of the areas I'm interested in
        plotting (eg. TTWA, or LSOA)
     Example: draw(growth, 'Growth', 'viridis', np.min(growth['Growth']),
        np.max(growth['Growth']))

     Note: it might be better to pass the shape/map files as explicit argument
     (right now, it just uses them assuming they are in the main workspace I think)
     '''

    if not (fig or ax):
        # if no figure or ax has been provided, then create one
        fig, ax = plt.subplots(figsize=(8,16))

    cmap = plt.get_cmap(color_scheme)
    norm = Normalize(vmin=data_min, vmax=data_max)

    # Lists of x,y bounds in order to set fig-ax lims
    xs = []
    ys = []

    # Plot the "container", that is the contours of the overall region
    # eg. plot GB
    if gb_filename:
        with fiona.open(gb_filename) as gb:
            for country in gb:
                if subset_outlines:
                    # if we only want a subset, check that at least one of the
                    # properties values (the specific key always changes) is
                    # present in the list of areas we want
                    if not set(country['properties'].values()).isdisjoint(subset_outlines):
                        # skip this iteration if not in wanted set
                        s = shape(country['geometry'])
                        p = PolygonPatch(s, color="lightgrey", edgecolor = [0,0,0])
                        ax.add_patch(p)
                        xs += [s.bounds[0],s.bounds[2]]
                        ys += [s.bounds[1],s.bounds[3]]
                else:
                    s = shape(country['geometry'])
                    p = PolygonPatch(s, color="lightgrey", edgecolor = [0,0,0])
                    ax.add_patch(p)
                    xs += [s.bounds[0],s.bounds[2]]
                    ys += [s.bounds[1],s.bounds[3]]

    # Plot NI, correcting for different east/northing zone
    if ni_filename:
        # if None, do not plot anything
        with fiona.open(ni_filename) as ni:
            # no need to check the subset because this is only to plot NI
             for country in ni:
                s = shape(country['geometry'])
                p = PolygonPatch(s, color="lightgrey")
                ax.add_patch(p)
                xs += [s.bounds[0],s.bounds[2]]
                ys += [s.bounds[1],s.bounds[3]]

    # Overlay ROIS, if non zero distances
    with fiona.open(shp_filename) as rois:
        # Plot TTWAs with colour
        for roi in rois:
            #NOTE: properties is always the same, the name of the column with
            # the code can change
            id_ = roi['properties'][shp_col]
            if id_ not in data[roi_col].values:
                continue
            row = data[data[roi_col] == id_]
            val = row[col].values[0]
            s = shape(roi['geometry'])
            p = PolygonPatch(s, color=cmap(norm(val)))
            xs += [s.bounds[0],s.bounds[2]]
            ys += [s.bounds[1],s.bounds[3]]
            ax.add_patch(p)
            #print(row)
    # Set bounds
    ax.set_xlim(min(xs),max(xs))
    ax.set_ylim(min(ys),max(ys))
    ax.axis('off')
    all_labels = [val for val in np.unique(data[col])]
    #select_labels = [np.min(all_labels), np.percentile(all_labels, 25),
#                    np.percentile(all_labels, 50),
#                     np.percentile(all_labels, 75), np.max(all_labels)]
    select_labels = np.linspace(data_min, data_max, 5)
    select_labels2 = [round(elem,2) for elem in select_labels]
    select_colors = [cmap(norm(val)) for val in select_labels]
    p1 = mpatches.Patch(color=select_colors[0], linewidth=0)
    p2 = mpatches.Patch(color=select_colors[1], linewidth=0)
    p3 = mpatches.Patch(color=select_colors[2], linewidth=0)
    p4 = mpatches.Patch(color=select_colors[3], linewidth=0)
    p5 = mpatches.Patch(color=select_colors[4], linewidth=0)
    plt.legend((p1,p2,p3,p4,p5,),
               (select_labels2[0],select_labels2[1],
               select_labels2[2], select_labels2[3], select_labels2[4],),
               fontsize = 14)
    if isinstance(data, dict):
        ax.set_xlabel(k)
    if params['SAVEFIG']:
        plt.savefig(params['file_name'])
    plt.draw() #plt.show()
    return fig, ax, xs, ys

def draw_map_and_landmarks(data, col, color_scheme, data_min, data_max,
             gb_filename, ni_filename,
             shp_filename, subset_outlines = None,
             landmarks = None, roi_col = 'TTWA code',
             shp_col = 'ttwa11cd', shp_name_col = 'ttwa11nm',
             params = {'SAVEFIG': False},
             fig = None, ax = None, add_names = False,
             marker_style = dict(color='tab:red', linestyle=':', marker='D',
                             markersize=8, markerfacecoloralt='tab:red',
                             fillstyle = 'full'),
            legend_args = dict(fontsize = '14')):

    if not (fig or ax):
        # if no figure or ax has been provided, then create one
        fig, ax = plt.subplots(figsize=(8,16))

    cmap = plt.get_cmap(color_scheme)
    norm = Normalize(vmin=data_min, vmax=data_max)

    # Lists of x,y bounds in order to set fig-ax lims
    xs = []
    ys = []
    order = []

    # Plot the "container", that is the contours of the overall region
    # eg. plot GB
    if gb_filename:
        with fiona.open(gb_filename) as gb:
            for country in gb:
                if subset_outlines:
                    # if we only want a subset, check that at least one of the
                    # properties values (the specific key always changes) is
                    # present in the list of areas we want
                    if not set(country['properties'].values()).isdisjoint(subset_outlines):
                        # skip this iteration if not in wanted set
                        s = shape(country['geometry'])
                        p = PolygonPatch(s, color="lightgrey")
                        ax.add_patch(p)
                        xs += [s.bounds[0],s.bounds[2]]
                        ys += [s.bounds[1],s.bounds[3]]
                else:
                    s = shape(country['geometry'])
                    p = PolygonPatch(s, color="lightgrey")
                    ax.add_patch(p)
                    xs += [s.bounds[0],s.bounds[2]]
                    ys += [s.bounds[1],s.bounds[3]]

    # Plot NI, correcting for different east/northing zone
    if ni_filename:
        # if None, do not plot anything
        with fiona.open(ni_filename) as ni:
            # no need to check the subset because this is only to plot NI
             for country in ni:
                s = shape(country['geometry'])
                p = PolygonPatch(s, color="lightgrey")
                ax.add_patch(p)
                xs += [s.bounds[0],s.bounds[2]]
                ys += [s.bounds[1],s.bounds[3]]

    # Overlay ROIS, if non zero distances
    with fiona.open(shp_filename) as rois:
        # Plot TTWAs with colour
        for roi in rois:
            #NOTE: properties is always the same, the name of the column
            # with the code can change
            id_ = roi['properties'][shp_col]
            if id_ not in data[roi_col].values:
                continue
            row = data[data[roi_col] == id_]
            val = row[col].values[0]
            s = shape(roi['geometry'])
            p = PolygonPatch(s, facecolor=cmap(norm(val)), linewidth = .5, edgecolor = [0,0,0])
            xs += [s.bounds[0],s.bounds[2]]
            ys += [s.bounds[1],s.bounds[3]]
            order.append(id_)
            ax.add_patch(p)
            if add_names:
                ax.text(np.mean(xs[-2:]), np.mean(ys[-2:]), #,id_,fontsize = 12)
                roi['properties'][shp_name_col],fontsize = 8)
            # Add a marker at the centroid if this ROI is a landmark
            if landmarks is not None:
                if id_ in landmarks:
                    ax.plot(np.mean(xs[-2:]), np.mean(ys[-2:]), **marker_style)
                    #                'markerfacecolor','r','markeredgecolor','r')
            #print(row)
    # Set bounds
    ax.set_xlim(min(xs),max(xs))
    ax.set_ylim(min(ys),max(ys))
    ax.axis('off')
    all_labels = [val for val in np.unique(data[col])]
    #select_labels = [np.min(all_labels), np.percentile(all_labels, 25),
#                     np.percentile(all_labels, 50),
#                     np.percentile(all_labels, 75), np.max(all_labels)]
    select_labels = np.linspace(data_min, data_max, 5)
    select_labels2 = [round(elem,2) for elem in select_labels]
    select_colors = [cmap(norm(val)) for val in select_labels]
    p1 = mpatches.Patch(color=select_colors[0], linewidth=0)
    p2 = mpatches.Patch(color=select_colors[1], linewidth=0)
    p3 = mpatches.Patch(color=select_colors[2], linewidth=0)
    p4 = mpatches.Patch(color=select_colors[3], linewidth=0)
    p5 = mpatches.Patch(color=select_colors[4], linewidth=0)
    plt.legend((p1,p2,p3,p4,p5,),
               (select_labels2[0],select_labels2[1],
               select_labels2[2], select_labels2[3], select_labels2[4],),
               **legend_args)
    if isinstance(data, dict):
        ax.set_xlabel(k)
    if params['SAVEFIG']:
        plt.savefig(params['file_name'])
    plt.draw() #plt.show()
    return fig, ax, xs, ys, s
