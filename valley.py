import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from mpl_toolkits.mplot3d import Axes3D
import time

# Function to generate points for a valley shape
def generate_valley_points(num_points):
    x = np.random.uniform(-5, 5, num_points)
    y = np.random.uniform(-5, 5, num_points)
    z = np.sin(np.sqrt(x**2 + y**2))  # Valley-like shape using a sine function
    return np.vstack((x, y, z)).T

class RealTimeVisualizer:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.scatter = self.ax.scatter([], [], [], c='b', marker='o', s=1)

        self.ax.set_xlim([-5, 5])
        self.ax.set_ylim([-5, 5])
        self.ax.set_zlim([-1, 1])
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Real-Time Lidar Data Visualization of a Valley')

        self.num_points = 100
        self.increment = 100
        self.max_points = 5000
        self.paused = False

        # Add sliders and buttons for interactivity
        self.add_controls()

    def add_controls(self):
        axcolor = 'lightgoldenrodyellow'
        ax_points = plt.axes([0.15, 0.01, 0.65, 0.03], facecolor=axcolor)
        ax_pause = plt.axes([0.85, 0.01, 0.1, 0.04])

        self.slider_points = Slider(ax_points, 'Points', 100, self.max_points, valinit=self.num_points, valstep=100)
        self.button_pause = Button(ax_pause, 'Pause')

        self.slider_points.on_changed(self.update_points)
        self.button_pause.on_clicked(self.toggle_pause)

    def update_points(self, val):
        self.num_points = int(val)

    def toggle_pause(self, event):
        self.paused = not self.paused
        self.button_pause.label.set_text('Resume' if self.paused else 'Pause')

    def visualize_valley_real_time(self):
        plt.ion()

        try:
            while self.num_points <= self.max_points:
                if not self.paused:
                    points = generate_valley_points(self.num_points)
                    self.scatter._offsets3d = (points[:, 0], points[:, 1], points[:, 2])
                    self.ax.set_title(f'Real-Time Lidar Data Visualization of a Valley (Points: {self.num_points})')
                    plt.draw()
                    plt.pause(0.1)  # Adjust the pause time as needed

                time.sleep(0.1)  # To prevent CPU overload

        except KeyboardInterrupt:
            print("Real-time visualization stopped.")

        plt.ioff()
        plt.show()

# Main function
if __name__ == "__main__":
    visualizer = RealTimeVisualizer()
    visualizer.visualize_valley_real_time()
