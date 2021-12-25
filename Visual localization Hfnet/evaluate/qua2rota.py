#import numpy as np
#
#def quaternion_to_rotation_matrix(quat):
#    q = quat.copy()
#    n = np.dot(q, q)
#    if n < np.finfo(q.dtype).eps:
#        return np.identity(4)
#    q = q * np.sqrt(2.0 / n)
#    q = np.outer(q, q)
#    rot_matrix = np.array(
#        [[1.0 - q[2, 2] - q[3, 3], q[1, 2] + q[3, 0], q[1, 3] - q[2, 0], 0.0],
#         [q[1, 2] - q[3, 0], 1.0 - q[1, 1] - q[3, 3], q[2, 3] + q[1, 0], 0.0],
#         [q[1, 3] + q[2, 0], q[2, 3] - q[1, 0], 1.0 - q[1, 1] - q[2, 2], 0.0],
#         [0.0, 0.0, 0.0, 1.0]],
#        dtype=q.dtype)
#    return rot_matrix
## 写上用四元数表示的orientation和xyz表示的position
#orientation = {'y': -0.6971278819736084, 'x': -0.716556549511624, 'z': -0.010016582945017661, 'w': 0.02142651612120239}
#position = {'y': -0.26022684372145516, 'x': 0.6453529828252734, 'z': 1.179122068068349}
#
#rotation_quaternion = np.asarray([orientation['w'], orientation['x'], orientation['y'], orientation['z']])
#translation = np.asarray([position['x'], position['y'], position['z']])
## 这里用的是UC Berkeley的autolab_core，比较方便吧，当然可以自己写一个fuction来计算，计算公式在https://www.cnblogs.com/flyinggod/p/8144100.html
#T_qua2rota =quaternion_to_rotation_matrix(rotation_quaternion)
#
#print(T_qua2rota)
 
import numpy as np
import math
from scipy.spatial.transform import Rotation as R
 
 
Rq=[-0.71934025092983234, 1.876085535681999e-06, 3.274841213980097e-08, 0.69465790385533299]
 
# 四元数到旋转矩阵
r = R.from_quat(Rq)
Rm = r.as_matrix()
# 0:array([ 1.00000000e+00, -2.74458557e-06,  2.55936079e-06])
# 1:array([-2.65358979e-06, -3.49007932e-02,  9.99390782e-01])
# 2:array([-2.65358979e-06, -9.99390782e-01, -3.49007932e-02])
 
# 符号相反的四元数, 仍表示同一个旋转
Rq1= [0.71934025092983234, -1.876085535681999e-06, -3.274841213980097e-08, -0.69465790385533299]
# 四元数到旋转矩阵
r1 = R.from_quat(Rq1)
Rm1 = r1.as_matrix()
# 0:array([ 1.00000000e+00, -2.74458557e-06,  2.55936079e-06])
# 1:array([-2.65358979e-06, -3.49007932e-02,  9.99390782e-01])
# 2:array([-2.65358979e-06, -9.99390782e-01, -3.49007932e-02])
 
# 四元数到欧拉角
euler0 = r.as_euler('xyz', degrees=True)
# ([-9.20000743e+01,  1.52039496e-04, -1.52039496e-04])
euler3 = r.as_euler('xzy', degrees=True)
#([-9.20000743e+01, -1.52039496e-04,  1.52039496e-04])
euler1 = r.as_euler('zxy', degrees=True)
#([-179.99564367,  -87.99992566,  179.99579836])
euler2 = r.as_euler('zyx', degrees=True)
#([ 1.57253169e-04,  1.46640571e-04, -9.20000743e+01])
 
euler4 = r.as_euler('yxz', degrees=True)
#([179.99564367, -87.99992566, 179.99549428])
 
euler5 = r.as_euler('yzx', degrees=True)
#([ 1.46640571e-04,  1.57253169e-04, -9.20000743e+01])
 
 
# 旋转矩阵到四元数
r3 = R.from_matrix(Rm)
qua = r3.as_quat()
#[0.7193402509298323, -1.8760855356819988e-06, -3.2748412139801076e-08, -0.694657903855333] #与原始相反,但等价
 
# 旋转矩阵到欧拉角
euler_1 = r3.as_euler('zxy', degrees=True)
#([-179.99564367,  -87.99992566,  179.99579836])
 
# 欧拉角到旋转矩阵
r4 = R.from_euler('zxy', [-179.99564367,  -87.99992566,  179.99579836], degrees=True)
rm = r4.as_matrix()
# 0:array([ 1.00000000e+00, -2.74452529e-06,  2.55936075e-06])
# 1:array([-2.65358765e-06, -3.49007933e-02,  9.99390782e-01])
# 2:array([-2.65352955e-06, -9.99390782e-01, -3.49007933e-02])
 
# 欧拉角到四元数
qua1 = r4.as_quat()
#([-7.19340251e-01,  1.87606384e-06,  3.27274889e-08,  6.94657904e-01])
 
 
#----测试--------------------------------------------------------------------
theta=[-116,    0. , -105]
r6 = R.from_euler('xyz', theta, degrees=True)
rm = r6.as_matrix()
# 0:array([-0.25881905, -0.42343401,  0.86816838])
# 1:array([-0.96592583,  0.1134588 , -0.23262502])
# 2:array([ 0.        , -0.89879405, -0.43837115])
 
qua3 = r6.as_quat()
#array([-0.52720286,  0.68706415, -0.39667667,  0.30438071])
 
print(Rm)
