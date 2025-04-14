"""

"""

import numpy as np
from numpy.typing import NDArray
from typing import Final
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

G: Final[float] = 6.67430e-11

class AstronomicalObject:
    def __init__(self,
                 mass: float,
                 radius: float,
                 position: NDArray[np.float64],
                 velocity: NDArray[np.float64],
                 static: bool = False):
        """
        Initialize an astronomical object.
        Parameters:
            mass (float): Mass of the object.
            radius (float): Radius of the object.
            position (np.ndarray[float]): Initial position array [x, y, z] of the object.
            velocity (np.ndarray[float]): Initial velocity vector [vx, vy, vz] of the object.
            static (bool): Whether the object is static or not.
        """
        assert position.shape == (3,) #Position must be an array with exactly three elements.
        assert velocity.shape == (3,) #Velocity must be an array with exactly three elements.
        self.mass: float = mass
        self.radius: float = radius
        self.position: np.ndarray[np.float64] = position
        self.velocity: np.ndarray[np.float64] = velocity
        self.static: bool = static
        self.trace_path: list[list[float]] = [position.tolist()]

def update_objects(astro_objects: list[AstronomicalObject], dt: float):
    if len(astro_objects) == 0:
        return

    # Store accelerations separately to maintain simultaneity
    accelerations = [np.array([0., 0., 0.]) for _ in astro_objects]

    # First calculate total accelerations on each object
    for i, astro_object in enumerate(astro_objects):
        if astro_object.static:
            continue
        total_acceleration = np.zeros(3)

        for j, other_astro_object in enumerate(astro_objects):
            if i == j:
                continue

            # Vector from astro_object to other_astro_object
            direction_vector = other_astro_object.position - astro_object.position
            dist = np.linalg.norm(direction_vector)
            if dist == 0:
                continue  # Safety check to avoid division by zero

            acc_magnitude = G * other_astro_object.mass / dist ** 2
            acc_vector = (direction_vector / dist) * acc_magnitude
            total_acceleration += acc_vector

        accelerations[i] = total_acceleration

    # Then update velocities and positions
    for astro_object, acc in zip(astro_objects, accelerations):
        if astro_object.static:
            continue

        astro_object.velocity += acc * dt
        astro_object.position += astro_object.velocity * dt
        astro_object.trace_path.append(astro_object.position.tolist())



if __name__ == "__main__":
    # Clearly defined constants and initial conditions
    AU = 149.6e9  # Astronomical Unit in meters
    DAY = 86400  # Seconds in a day

    # Astronomical objects clearly defined and realistic
    objects = [
        # Sun (massive center object)
        AstronomicalObject(
            mass=1.989e30,
            radius=696340e3,
            position=np.array([0., 0., 0.]),
            velocity=np.array([0., 0., 0.]),
            static=True),  # Sun as central, static object for simplicity

        # Earth in circular orbit around Sun at 1 AU
        AstronomicalObject(
            mass=5.972e24,
            radius=6371e3,
            position=np.array([AU, 0., 0.]),
            velocity=np.array([0., 29.78e3, 0.])),  # Earth's orbital velocity ~29.78 km/s

        # Moon orbiting Earth (combined Earth velocity plus Moon orbital velocity around Earth)
        AstronomicalObject(
            mass=7.348e22,
            radius=1737e3,
            position=np.array([AU + 384.4e6, 0., 0.]),
            velocity=np.array([0., 29.78e3 + 1.022e3, 0.])),  # Earth's velocity + Moon's relative
    ]

    # Clearly choose a stable timestep; 1 hour (3600 seconds) is suitable for solar system scale
    dt = 3600  # One hour per step in seconds

    # Simulate clearly for one year (approximately 365 days)
    time_steps = int((365 * DAY) / dt)

    for _ in range(time_steps):
        update_objects(objects, dt)

    # Visualize results clearly
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    colors = ['yellow', 'blue', 'gray']  # Sun-yellow, Earth-blue, Moon-gray
    labels = ['Sun', 'Earth', 'Moon']

    for idx, obj in enumerate(objects):
        path_array = np.array(obj.trace_path)
        ax.plot3D(path_array[:, 0], path_array[:, 1], path_array[:, 2],
                  label=f'{labels[idx]} Orbit', color=colors[idx])
        ax.scatter(path_array[-1, 0], path_array[-1, 1], path_array[-1, 2],
                   s=obj.radius * 0.00001, color=colors[idx], marker='o', edgecolors='k')

    # Proper axis scaling for clear display
    all_positions = np.concatenate([obj.trace_path for obj in objects])
    max_range = np.ptp(all_positions, axis=0).max()
    mid = np.mean(all_positions, axis=0)

    ax.set_xlim(mid[0] - max_range / 2, mid[0] + max_range / 2)
    ax.set_ylim(mid[1] - max_range / 2, mid[1] + max_range / 2)
    ax.set_zlim(mid[2] - max_range / 2, mid[2] + max_range / 2)

    # Labeling and legend for clarity
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_zlabel('Z (meters)')
    ax.set_title("Orbit of Earth and Moon around Sun")
    ax.legend()
    plt.show()

