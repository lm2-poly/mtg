"""
-------------------------------------------------------------------------------------------------------------------------
Multinozzle Toolpath Generator (MTG) for FACMO Chair multinozzle printhead
(mathTools.py)

Author : Jean-François Chauvette, M.Sc.A, PhD candidate
Email : jean-francois.chauvette@polymtl.ca, chauvettejf@gmail.com
Project : FACMO Chair - Objective 4

Laboratory for Multiscale Mechanics (LM2)
Date created : 2022-03-28

Definition:
    Mathematic functions for MTG
    
-------------------------------------------------------------------------------------------------------------------------
Update notes

Date		    Notes
¯¯¯¯¯¯¯¯¯¯		¯¯¯¯¯¯¯¯¯¯
2022-11-16		Moved all basic math functions of the MTG in its own script

-------------------------------------------------------------------------------------------------------------------------
"""

# ========================================================================================
# IMPORTS
# ========================================================================================
import numpy as np
import math as m

# ========================================================================================
# FUNCTION DEFINITIONS
# ========================================================================================

# Function unit_vector
#
#   Description: returns a unit vector
#
#   Returns:
#       unit vector or None if norm is null
#
#   Parameters:
#       vector : np.array, the non-normalized vector
#
def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    if np.linalg.norm(vector) != 0:
        return vector / np.linalg.norm(vector)
    else:
        return None

# Function distanceP1P2
#
#   Description: get the distance and direction vector between two points
#
#   Returns: 
#       dist : float, the 3D euclidean distance between p1 and p2
#       dir_vect : np.array, the direction vector components between p1 and p2
#
#   Parameters:
#       p1 : list, the [x,y,z] coordinates of p1. Starting point of dir_vect.
#       p2 : list, the [x,y,z] coordinates of p2. Ending point of dir_vect.
#       normalize : bool, set to True to return the normalized direction vector
#
def distanceP1P2(p1, p2, normalize = False):
    # Get the vector between two points
    dir_vect = np.array(p2) - np.array(p1)
    
    # Calculate distance from P1 to P2
    dist = np.linalg.norm(dir_vect)
    
    # Normalization of the direction vector
    if normalize:
        dir_vect = unit_vector(dir_vect)
    
    return dist, dir_vect

# Function projectVector
#
#   Description: projects the vector u on v in 3D space.
#
#   Returns:
#       proj_of_u_on_v : np.array, the projected vector of u on v
#
#   Parameters:
#       u : np.array, the vector to project on v
#       v : np.array, the vector on which to project u
#
def projectVector(u, v):
    # finding norm of the vector v
    v_norm = np.linalg.norm(v)

    # find dot product using np.dot()
    proj_of_u_on_v = (np.dot(u, v)/v_norm**2)*v
    return proj_of_u_on_v
  
# Function getRotMat
#
#   Description: calculates the rotation matrix required to obtain the orientation
#                of the triad with respect to the ref frame.
#
#   Returns:
#       rotMat : np.matrix, the resulting rotation matrix
#
#   Parameters:
#       triad : np.matrix, the rotated triad
#       refFrame : np.matrix, the referential matrix
#
def getRotMat(triad, refFrame = None):
    # By default, the reference frame is the coordinate system X Y Z at the origin around which the triad is rotated
    if refFrame == None:
        refFrame = np.matrix([[1, 0, 0],
                              [0, 1, 0],
                              [0, 0, 1]])

    # rotMat calculation using linear algebra
    rotMat = triad.T*np.linalg.inv(refFrame.T)
    return rotMat

# Function rotAroundNormal
#
#   Description: generate a rotation around the normal vector of a triad using
#                an associated rotation matrix and angle around the normal.
#
#   Returns:
#       newTriad.T : np.matrix, the transpose of the new calculated triad matrix
#
#   Parameters:
#       triad : np.matrix, the rotated triad
#       rotMat : np.matrix, the associated rotation matrix
#       angle : float, the desired angle theta (deg) around the normal
#
def rotAroundNormal(triad, rotMat, angle):
    # Triad and rotMat are of type : np.matrix
    refFrame = triad.T*np.linalg.inv(rotMat) # the triad at rotations = 0
    refFrame = Rz(m.radians(-angle))*refFrame # rotating the reference frame around Z by angle value
    newTriad = rotMat*refFrame # replacing the newly rotated reference frame at the triad original location
    return newTriad.T

# Functions Rx, Ry, Rz
#
#   Description: calculate the individual rotation matrix around x, y or z using a theta angle (rad).
#
#   Returns:
#       np.matrix, the resulting rotation matrix
#
#   Parameters:
#       angle : float, the desired angle (rad) around the corresponding axis
#
def Rx(angle):
  return np.matrix([[ 1, 0           , 0           ],
                    [ 0, m.cos(angle),-m.sin(angle)],
                    [ 0, m.sin(angle), m.cos(angle)]])

def Ry(angle):
  return np.matrix([[ m.cos(angle), 0, m.sin(angle)],
                    [ 0           , 1, 0           ],
                    [-m.sin(angle), 0, m.cos(angle)]])

def Rz(angle):
  return np.matrix([[ m.cos(angle), -m.sin(angle), 0 ],
                    [ m.sin(angle), m.cos(angle) , 0 ],
                    [ 0           , 0            , 1 ]])

# Function heronRadius
#
#   Description : Calculated the circle radius which contains the 3 given coordinates
#
#   Returns:
#       float, the calculated radius
#
#   Parameters:
#       t : list, the list of three points
#
def heronRadius(t):
    # Vectors contained in the circle
    a = np.linalg.norm(t[1]-t[0])
    b = np.linalg.norm(t[2]-t[1])
    c = np.linalg.norm(t[2]-t[0])
    p = (a+b+c)/2
    s = np.sqrt(p*(p-a)*(p-b)*(p-c))
    
    # Sinus law to return the radius value
    return (a*b*c)/(4*s)
