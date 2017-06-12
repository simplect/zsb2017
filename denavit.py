from numpy import *
from sympy import *
from scipy.optimize import minimize

# Denavit-Hartenberg Matrix as found on Wikipedia "Denavit-Hartenberg parameters"
def DenHarMat(theta, alpha, a, d):
    cos_theta = cos(theta)
    sin_theta = sin(theta)
    cos_alpha = cos(alpha)
    sin_alpha = sin(alpha)


    return array([
        [cos_theta, -sin_theta*cos_alpha, sin_theta*sin_alpha, a*cos_theta],
        [sin_theta, cos_theta*cos_alpha, -cos_theta*sin_alpha, a*sin_theta],
        [0, sin_alpha, cos_alpha, d],
        [0, 0, 0, 1],
    ])

i1 = DenHarMat(pi/2, -pi/2, 0, -1)
i2 = DenHarMat(pi/4, pi/2, -sqrt(2), 1)
i3 = DenHarMat(-pi/2, pi/4, 1, 0)
print(i1)
print(i2)
print(i3)
