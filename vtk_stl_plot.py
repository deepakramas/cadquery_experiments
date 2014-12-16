# Using code from http://nbviewer.ipython.org/urls/bitbucket.org/somada141/pyscience/raw/master/20140910_RayCasting/Material/PythonRayCastingSphereVTK.ipynb

import os
import vtk

def loadSTL(filenameSTL):
    readerSTL = vtk.vtkSTLReader()
    readerSTL.SetFileName(filenameSTL)
    # 'update' the reader i.e. read the .stl file
    readerSTL.Update()

    polydata = readerSTL.GetOutput()

    # If there are no points in 'vtkPolyData' something went wrong
    if polydata.GetNumberOfPoints() == 0:
        raise ValueError(
            "No point data could be loaded from '" + filenameSTL)
        return None
    
    return polydata

from IPython.display import Image
def vtk_show(renderer, width=400, height=300):
    """
    Takes vtkRenderer instance and returns an IPython Image with the rendering.
    """
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetOffScreenRendering(1)
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(width, height)
    renderWindow.Render()
     
    windowToImageFilter = vtk.vtkWindowToImageFilter()
    windowToImageFilter.SetInput(renderWindow)
    windowToImageFilter.Update()
     
    writer = vtk.vtkPNGWriter()
    writer.SetWriteToMemory(1)
    writer.SetInputConnection(windowToImageFilter.GetOutputPort())
    writer.Write()
    data = str(buffer(writer.GetResult()))
    
    return Image(data)

def plot_stl(filename, position=[0,0,1], viewAngle = 30, background = [1,1,1], opacity=0.25,width=400, height=300):
    """
    Plots stl files via vtk in Ipython
    """
    myCamera = vtk.vtkCamera()
    myCamera.SetViewAngle(viewAngle)
    myCamera.SetPosition(position[0],position[1],position[2])
    mapper = vtk.vtkPolyDataMapper()
    mesh = loadSTL(filename)
    mapper.SetInput(mesh)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetOpacity(opacity)

    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(background[0], background[1], background[2])
    renderer.SetActiveCamera(myCamera)
    return vtk_show(renderer)