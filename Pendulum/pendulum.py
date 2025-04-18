# pendulum.py
# Created On: 2025-03-21
# Created By: Edward Cromwell
# An exploration of the motion of a pendulum using numerical methods

import numpy as np
from typing import Final
from matplotlib import pyplot as plt

g: Final[float] = 9.8 # gravity approximation

class Pendulum:
    def __init__(self, L: float, theta_0: float, omega_0: float, mu: float):
        self.L: float = L # length of pendulum
        self.theta: float = theta_0 # initial angle
        self.omega: float = omega_0 # initial angular velocity
        self.mu: float = mu # damping factor
        self.trace_path: list[list[float]] = [[self.theta, self.omega]]
    
    # describes angular velocity of a pendulum
    def theta_dot(self, step: float):
        self.theta += self.omega * step

    # describes angular acceleration of a pendulum
    def theta_double_dot(self, step: float):
        self.omega += (-(self.mu * self.omega) - ((g / self.L) * np.sin(self.theta))) * step

    # updates position of the pendulum
    def update_theta(self, T: float, step: float):
        for t_i in np.arange(0, T, step):
            self.theta_double_dot(step)
            self.theta_dot(step)
            self.trace_path.append([self.theta,self.omega])

    # convert trace path to numpy array
    def get_trace_path(self):
        return np.array(self.trace_path)

if __name__ == "__main__":
    p = Pendulum(L=1, theta_0=np.pi / 3, omega_0=0, mu=0.5)
    p.update_theta(T=100, step=0.01)

    trace_path = p.get_trace_path()

    plt.figure(figsize=(5, 5))
    plt.plot(trace_path[:, 0], trace_path[:, 1], label='Theta')
    plt.title('Angular Velocity vs Angle')
    plt.xlabel('Angle (radians)')
    plt.ylabel('Angular Velocity (rad/s)')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()