"""
-------------------------------------------------------------------------------------------------------------------------
Multinozzle Toolpath Generator (MTG) for FACMO Chair multinozzle printhead
(interpolate_surface_from_stl.py)

Author : Jean-François Chauvette, M.Sc.A, PhD candidate
Email : jean-francois.chauvette@polymtl.ca, chauvettejf@gmail.com
Project : FACMO Chair - Objective 4

Laboratory for Multiscale Mechanics (LM2)
Date created : 2022-04-20

Definition:
    Implementation of the NURBS-Python module for fitting a NURBS surface
    using a scanned mesh saved as an STL file.
    
    The mesh of the STL file must be a perfectly ordered grid of vertices that
    conforms to the scanned surface. One can fit such grid over a scanned mesh
    using the shrinkwrap modifier in the Blender modeling software.
    
-------------------------------------------------------------------------------------------------------------------------
Update notes

Date		    Notes
¯¯¯¯¯¯¯¯¯¯		¯¯¯¯¯¯¯¯¯¯
2022-11-17		Polished the script + added comments and header

-------------------------------------------------------------------------------------------------------------------------
"""

# ========================================================================================
# IMPORTS
# ========================================================================================
# Orbingol modules
from geomdl import *
from geomdl.visualization import VisMPL as vis

# Common modules
import numpy as np
from stl import mesh
import matplotlib.pyplot as plt

# MTG imports
from mtg_modules.sort_vertices import *

# ========================================================================================
# FUNCTION DEFINITIONS
# ========================================================================================

# Function interpolate_surface_from_stl
#
#   Description: Interpolate a NURBS surface from an STL file
#
#   Returns:
#       surf : the NURBS-Python surface object
#
#   Parameters:
#       file : mesh, imported STL file
#       usize : int, number of control points along u
#       vsize : int, number of control points along v
#       udeg : int, spline degree along u
#       vdeg : int, spline degree along v
#       eval_delta : int, delta value of the uv pair to evaluate the surface
#       export_json = True : bool, set to True to export a json file of the surface
#       render_surf = False : bool, set to True to plot the surface in matplotlib
#       render_eval = False : bool, set to True to plot the evaluated points in matplotlib
#
def interpolate_surface_from_stl(file, usize, vsize, udeg, vdeg, eval_delta, export_json = True, render_surf = False, render_eval = False):
    # Check if the file is in STL format
    if file.find('.stl') == -1:
        raise Exception('Error: the file to import must be in STL format.')
        
    # import the mesh from an STL file
    myMesh = mesh.Mesh.from_file(file)

    # Rearrange the coordinates (XYZ) of the STL to be used for interpolation
    points = np.around(np.unique(myMesh.vectors.reshape([int(myMesh.vectors.size/3), 3]), axis=0),2).tolist()
    
    # Sort the points list to be used for surface interpolation
    points = sortUV(points,usize,vsize)

    surf = fitting.interpolate_surface(points, usize, vsize, udeg, vdeg)
    surf.delta = eval_delta

    # Export the surface data in json format to reuse later using import_json
    if export_json:
        exchange.export_json(surf, file[0:file.find('.stl')] + '.json')
        
    # Render the interpolated surface
    if render_surf:
        surf.vis = vis.VisSurface()
        surf.render()
    
    # Visualize data and evaluated points together
    if render_eval:
        evalpts = np.array(surf.evalpts)
        pts = np.array(points)
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.scatter(evalpts[:, 0], evalpts[:, 1], evalpts[:, 2])
        ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], color="red")
        plt.show()
    
    # Return the interpolate surface object
    return surf    