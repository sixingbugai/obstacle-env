from __future__ import print_function
from __future__ import division
import numpy as np
from scipy import signal


class Dynamics1D(object):
    """
        A fourth-order one-dimensional dynamical system.
    """
    def __init__(self):
        self.A = self.B = self.C = self.D = None
        self.discrete = self.continuous = None

        self.continuous_dynamics()
        self.discrete_dynamics()

    def continuous_dynamics(self):
        """
            Continuous state-space model
        """
        self.A = [[0, 1, 0, 0],
                  [0, -self.Cx, 1, 0],
                  [0, 0, 0, 1],
                  [0, 0, -self.w0**2, -2*self.zeta*self.w0]]
        self.B = [[0], [0], [0], [self.w0**2]]
        self.C = np.identity(np.shape(self.A)[0])
        self.D = np.zeros(np.shape(self.B))

        self.continuous = (self.A, self.B, self.C, self.D)

    def discrete_dynamics(self):
        """
            Discrete state-space model
        """

        self.discrete = signal.cont2discrete(self.continuous, self.dt, method='zoh')

    def step(self, state, command):
        """
            Step the dynamics
        """
        return np.dot(self.discrete[0], state)+np.dot(self.discrete[1], command)


class Dynamics2D(Dynamics1D):
    """
        A fourth-order two-dimensional dynamical system.
    """
    def __init__(self):
        super(Dynamics2D, self).__init__()

        self.continuous_dynamics()
        self.discrete_dynamics()

    def continuous_dynamics(self):
        """
            Continuous state-space model
        """
        a, b = self.A, self.B

        self.A = np.vstack((np.hstack((np.array(a), np.zeros(np.shape(a)))),
                            np.hstack((np.zeros(np.shape(a)), np.array(a)))))
        self.B = np.vstack((np.hstack((np.array(b), np.zeros(np.shape(b)))),
                            np.hstack((np.zeros(np.shape(b)), np.array(b)))))
        self.C = np.identity(np.shape(self.A)[0])
        self.D = np.zeros(np.shape(self.B))

        self.continuous = (self.A, self.B, self.C, self.D)