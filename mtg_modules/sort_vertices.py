"""
-------------------------------------------------------------------------------------------------------------------------
Multinozzle Toolpath Generator (MTG) for FACMO Chair multinozzle printhead
(sort_vertices.py)

Author : Jean-François Chauvette, M.Sc.A, PhD candidate
Email : jean-francois.chauvette@polymtl.ca, chauvettejf@gmail.com
Project : FACMO Chair - Objective 4

Laboratory for Multiscale Mechanics (LM2)
Date created : 2022-04-18

Definition:
    The script allows the sorting of a list of vertices coordinates given as list [x,y,z]
    in ascending order of x and then acsending order of y inside each of the already sorted
    rows and columns parametrized by the grid size u × v.
    
-------------------------------------------------------------------------------------------------------------------------
Update notes

Date		    Notes
¯¯¯¯¯¯¯¯¯¯		¯¯¯¯¯¯¯¯¯¯
2022-11-17		Polished the script + added comments and header

-------------------------------------------------------------------------------------------------------------------------
"""

# ========================================================================================
# FUNCTION DEFINITIONS
# ========================================================================================

# Function sort_u, sort_v
#
#   Description: The functions return the coordinate index for which to sort the coordinate
#                   using the sortUV function.
#
#   Returns:
#       point[0], point[1] : the coordinate index
#
#   Parameters:
#       point : the vertice to sort in the list
#
def sort_u(point):
    return point[0]

def sort_v(point):
    return point[1]

# Function sort_u, sort_v
#
#   Description: The function calls the sorting functions to order the vertices of the grid
#                   that will be used to fit the NURBS surface
#
#   Returns:
#       finalList : float list, the list of sorted coordinates given as [[x1,y1,z1], ..., [xn,yn,zn]]
#
#   Parameters:
#       myList : float list, n coordinates given as [[x1,y1,z1], ..., [xn,yn,zn]]
#       u : the grid size following the u-direction. same as the number of control points of a reconstructed surface.
#       v : the grid size following the v-direction. same as the number of control points of a reconstructed surface.
#
def sortUV(myList, u, v):
    finalList = []
    myList.sort(key=sort_u)
    for i in range(u):
        temp = myList[i*v:(i+1)*v]
        temp.sort(key=sort_v)
        for j in temp:
            finalList.append(j)
    return finalList