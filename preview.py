# @Time : 2022/3/23 15:53
# @Author : Deng Xutian
# @Email : dengxutian@126.com


import tf
import vtk
import time
import numpy as np
import matplotlib.pyplot as plt
# import scipy.spatial.transform.rotation as R
from scipy.spatial.transform import Rotation as R


class preview():
    
    def __init__(self):
        
        data = []
        file = open('preview.txt')
        lines = file.readlines()
        for line in lines:
            line = line.split(' ')
            line = line[2:]
            data.append(line)
        self.data = np.array(data)
        self.data = self.data.astype(np.float64)

        euler = []
        quaternion = self.data[:, 0:4]
        for i in range(quaternion.shape[0]):
            euler.append(R(quaternion[i,:]).as_euler('xyz', degrees=True))
        self.euler = np.array(euler)


    def preview_pose(self):
            
            # model_offset_1 = -38
            # model_offset_2 = -16
            # model_offset_3 = 128
            # model_rotate = -90

            model_offset_1 = -38
            model_offset_2 = -128
            model_offset_3 = -16
            model_rotate = 90

            reader = vtk.vtkSTLReader()
            reader.SetFileName('probe.STL')

            transform = vtk.vtkTransform()
            transform.RotateX(model_rotate)
            transform.Translate(model_offset_1, model_offset_2, model_offset_3)
            # transform.RotateX(model_rotate)

            transformFilter = vtk.vtkTransformPolyDataFilter()
            transformFilter.SetInputConnection(reader.GetOutputPort())
            transformFilter.SetTransform(transform)
            transformFilter.Update()

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(transformFilter.GetOutputPort())

            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.SetScale(0.1, 0.1, 0.1)
            actor.GetProperty().SetColor(150 / 255.0, 150 / 255.0, 150 / 255.0)
            actor.GetProperty().SetOpacity(0.6)

            xyz_axes = vtk.vtkAxesActor()
            xyz_axes.SetPosition(0, 0, 0)
            xyz_axes.SetTotalLength(20, 20, 20)

            ren = vtk.vtkRenderer()
            ren.AddActor(actor)
            ren.AddActor(xyz_axes)


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
            # camera.SetClippingRange(1, 1)
            # camera.SetViewAngle(60)
            camera.SetPosition(10, 10, 10)
            camera.SetFocalPoint(0, 0, 0)
            camera.Roll(235)
            camera.ComputeViewPlaneNormal()

            ren.SetActiveCamera(camera)
            ren.ResetCamera()
            ren.SetBackground(0 / 255.0, 0 / 255.0, 0 / 255.0)

            
            renWin = vtk.vtkRenderWindow()
            renWin.AddRenderer(ren)
            renWin.SetSize(800, 800)
            renWin.Render()

            # iren = vtk.vtkRenderWindowInteractor()
            # iren.SetRenderWindow(renWin)
            # iren.Initialize()
            # iren.Start()

            wif = vtk.vtkWindowToImageFilter()
            wif.SetInput(renWin)
            wif.Update()

            writer = vtk.vtkOggTheoraWriter()
            writer.SetFileName('preview.ogv')
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

    def preview_force(self):

        plt.clf()
        plt.plot(np.arange(self.data.shape[0])/10, self.data[:,4])
        plt.xlabel('Time (s)')
        plt.ylabel('Force X (N)')
        plt.savefig('force_x', dpi=600)

        plt.clf()
        plt.plot(np.arange(self.data.shape[0])/10, self.data[:,5])
        plt.xlabel('Time (s)')
        plt.ylabel('Force Y (N)')
        plt.savefig('force_y', dpi=600)
        
        plt.clf()
        plt.plot(np.arange(self.data.shape[0])/10, self.data[:,6])
        plt.xlabel('Time (s)')
        plt.ylabel('Force Z (N)')
        plt.savefig('force_z', dpi=600)

        plt.clf()
        plt.plot(np.arange(self.data.shape[0])/10, self.data[:,7])
        plt.xlabel('Time (s)')
        plt.ylabel('Torque X (N*m)')
        plt.savefig('torque_x', dpi=600)

        plt.clf()
        plt.plot(np.arange(self.data.shape[0])/10, self.data[:,8])
        plt.xlabel('Time (s)')
        plt.ylabel('Torque Y (N*m)')
        plt.savefig('torque_y', dpi=600)

        plt.clf()
        plt.plot(np.arange(self.data.shape[0])/10, self.data[:,9])
        plt.xlabel('Time (s)')
        plt.ylabel('Torque Z (N*m)')
        plt.savefig('torque_z', dpi=600)


if __name__ == '__main__':
    print('Previewing')
    demo = preview()
    demo.preview_pose()
    demo.preview_force()
    print('Finish!')
