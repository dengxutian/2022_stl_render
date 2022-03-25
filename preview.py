# @Time : 2022/3/23 15:53
# @Author : Deng Xutian
# @Email : dengxutian@126.com


import tf
import vtk
import time
import numpy as np
import scipy.spatial.transform.rotation as R

class preview():
    
    def __init__(self):
        euler = []
        quaternion = np.load('quaternion.npy')
        for i in range(quaternion.shape[0]):
            euler.append(R.Rotation(quaternion[i,:]).as_euler('xyz', degrees=True))
        self.euler = np.array(euler)


    def show(self):
            
            model_offset_1 = -38
            model_offset_2 = -16
            model_offset_3 = 128

            reader = vtk.vtkSTLReader()
            reader.SetFileName('probe.STL')

            transform = vtk.vtkTransform()
            transform.Translate(model_offset_1, model_offset_2, model_offset_3)
            transform.RotateX(-90)

            transformFilter = vtk.vtkTransformPolyDataFilter()
            transformFilter.SetInputConnection(reader.GetOutputPort())
            transformFilter.SetTransform(transform)
            transformFilter.Update()

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(transformFilter.GetOutputPort())

            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.SetScale(0.1, 0.1, 0.1)
            actor.GetProperty().SetColor(220 / 255.0, 220 / 255.0, 220 / 255.0)
            # actor.GetProperty().SetOpacity(0.6)

            ren = vtk.vtkRenderer()
            ren.AddActor(actor)


            # axes = vtk.vtkAxesActor()
            # axes.SetPosition(0, 0, 0)
            # axes.SetTotalLength(50, 50, 50)
            # axes.SetShaftType(1)
            # axes.SetAxisLabels(1)
            # axes.SetCylinderRadius(0.02)
            # axes_transform = vtk.vtkTransform()
            # axes_transform.Translate(0, 50, 0)
            # axes.SetUserTransform(axes_transform)

            camera = vtk.vtkCamera()
            camera.SetClippingRange(1, 1)
            camera.SetViewUp(0, 0, 0)
            camera.SetPosition(0, 0, -1000)
            camera.SetFocalPoint(0, 0, 1)
            # camera.Roll(70)
            camera.ComputeViewPlaneNormal()

            ren.SetActiveCamera(camera)
            ren.ResetCamera()
            ren.SetBackground(0 / 255.0, 0 / 255.0, 0 / 255.0)

            renWin = vtk.vtkRenderWindow()
            renWin.AddRenderer(ren)
            renWin.SetSize(1920, 1080)
            renWin.Render()

            wif = vtk.vtkWindowToImageFilter()
            wif.SetInput(renWin)
            wif.Update()

            writer = vtk.vtkOggTheoraWriter()
            writer.SetFileName('test.ogv')
            writer.SetInputConnection(wif.GetOutputPort())
            writer.Start()
            writer.Write()

            for i in range(self.euler.shape[0]):

                actor.RotateX(self.euler[i,0])
                actor.RotateY(self.euler[i,1])
                actor.RotateZ(self.euler[i,2])

                renWin.Render()

                wif.Modified()
                writer.Write()

                actor.RotateZ(-self.euler[i,2])
                actor.RotateY(-self.euler[i,1])
                actor.RotateX(-self.euler[i,0])

                print(time.time())
                time.sleep(0.01)
            writer.End()


if __name__ == '__main__':
    demo = preview()
    demo.show()