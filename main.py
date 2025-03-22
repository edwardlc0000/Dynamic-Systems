# main.py: This file contains the 'main' function.Program execution begins and ends there.
# Created On: 2025-03-15
# Created By: Edward Cromwell
# An exploration of dyanmic systems in Python.

import pendulum
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("Hello from dynamic-systems!")

    p = pendulum.Pendulum(L=1, theta_0=np.pi/3, omega_0=0, mu=0.5)
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

if __name__ == "__main__":
    main()
