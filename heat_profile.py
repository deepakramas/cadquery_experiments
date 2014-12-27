
# coding: utf-8

## Generating and Visualizing STL files from cadquery

# In[31]:

from cadquery import *


### Method for defining points on a circle

# In[32]:

import numpy as np
def getPointsOnCircle(n,radius):
    angles = np.linspace(0,2*np.pi,n,False)
    x = radius*np.cos(angles)
    y = radius*np.sin(angles)
    return zip(x,y)


### Use CADquery to generate a prismatic circle with holes arranged around center

# In[38]:

def createCircleWithHoles(n,holeCenterRadius=1.5):
    circleRadius = 2.0
    holeRadius = 0.25
    radius1 = holeCenterRadius - holeRadius
    radius2 = holeRadius
    maxNumCircles = 2*np.pi / np.arccos(((radius1+radius2)**2 - 2*radius2**2) / (radius1+radius2)**2) 
    if n >= (maxNumCircles-1):
        print 'Max num circles possible = ' + str(maxNumCircles)
        return
    if (holeCenterRadius + holeRadius) >= (circleRadius-0.5):
        print "circles do not fit into circle"
        return
    pts = getPointsOnCircle(n,holeCenterRadius)
    r = Workplane("front").circle(circleRadius) # make base
    r = r.pushPoints(pts)     # points are on the stack
    r = r.circle(holeRadius)      # circle will operate on all points
    extrudeDistance = 1.
    r = r.extrude(extrudeDistance)  # make prism
    r2 = Workplane("front").center(0,-circleRadius).rect(3,0.25)
    r2 = r2.extrude(extrudeDistance)
    r = r.cut(r2)
    if radius1 <= 0.6:
        print 'overlap with loft'
        return
    result = r.faces("Z>").circle(0.5).workplane(offset=0.25).circle(0.5).loft(combine=True)
    return exporters.toString(result,'STL')


def main(n=2,holeCenterRadius=1.5):
    return createCircleWithHoles(n,holeCenterRadius)

import sys
if __name__ == '__main__':
    main(int(sys.argv[1]),float(sys.argv[2]))


