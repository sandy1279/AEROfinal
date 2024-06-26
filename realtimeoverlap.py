import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import cv2
import time
# Function to generate points for a valley shape
def generate_valley_points(num_points):
    x = np.random.uniform(-5, 5, num_points)
    y = np.random.uniform(-5, 5, num_points)
    z = np.sin(np.sqrt(x**2 + y**2))  # Valley-like shape using a sine function
    return np.vstack((x, y, z)).T

class RealTimeVisualizer:
    def __init__(self, img_path):
        self.fig, self.ax = plt.subplots()
        self.scatter = self.ax.scatter([], [], c='b', s=10)

        # Load and preprocess the image
        self.img = self.preprocess_image(cv2.imread(img_path))
        self.img_h, self.img_w, _ = self.img.shape
        self.ax.imshow(self.img)

        self.num_points = 100
        self.increment = 100
        self.max_points = 5000
        self.paused = False

        # Add sliders and buttons for interactivity
        self.add_controls()

    def preprocess_image(self, img):
        # Convert to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Resize image for consistency
        target_size = (800, 600)  # Adjust size as needed
        img = cv2.resize(img, target_size)
        
        # Optionally adjust contrast and brightness
        alpha = 1.2  # Contrast control (1.0-3.0)
        beta = 50    # Brightness control (0-100)
        img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

        return img

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

    def project_points_to_image(self, points):
        # Normalize the x, y coordinates to fit the image dimensions
        x = np.clip(((points[:, 0] + 5) / 10) * self.img_w, 0, self.img_w - 1).astype(int)
        y = np.clip(((points[:, 1] + 5) / 10) * self.img_h, 0, self.img_h - 1).astype(int)
        return x, y

    def visualize_valley_real_time(self):
        plt.ion()

        try:
            while self.num_points <= self.max_points:
                if not self.paused:
                    points = generate_valley_points(self.num_points)
                    x, y = self.project_points_to_image(points)

                    # Update scatter plot with new points
                    self.scatter.set_offsets(np.c_[x, y])

                    # Color points based on their z-value to give a depth perception
                    colors = (points[:, 2] - points[:, 2].min()) / (points[:, 2].max() - points[:, 2].min())
                    self.scatter.set_array(colors)
                    self.scatter.set_cmap('viridis')
                    
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
    image_path = 'testimage.png'  # Provide the path to your valley image here
    visualizer = RealTimeVisualizer(image_path)
    visualizer.visualize_valley_real_time()
