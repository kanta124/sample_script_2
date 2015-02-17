#-------------------------------------------------------------------------------
# Name:    fiber_layout_0502(proc)
# Purpose: define fiber layout in ITECH pavilion
#
# Author:  Kantaro MAKANAE(referenced from Kenryo TAKAHASHI & Vangel KUKOV)
#
# Created: 02/05/2014
#-------------------------------------------------------------------------------

import rhinoscriptsyntax as rs
import math
import random

points = []
crvTrails = [] #crvs from each worms
for worm in wormsInitial:
    points.append(worm.Move())
    crvTrails.append(worm.Draw())
    step = worm.step