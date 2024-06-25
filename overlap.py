import numpy as np
import cv2
import open3d as o3d

# Assume intrinsic parameters of the RGB camera are known (replace with your actual parameters)
camera_intrinsics = {
    'fx': 600, 'fy': 600, 'cx': 320, 'cy': 240,
    'dist_coeffs': np.zeros(5)  # assuming no distortion for simplicity
}

# Assume extrinsic parameters (rotation and translation) are known (replace with your actual parameters)
rotation_matrix = np.array([[0.9998, -0.0175, 0.0015],
                            [0.0175, 0.9998, -0.0045],
                            [-0.0013, 0.0046, 0.9999]])
translation_vector = np.array([0.1, 0.0, 0.15])

def project_point_cloud_to_image(point_cloud, rotation_matrix, translation_vector, camera_intrinsics):
    fx, fy, cx, cy = camera_intrinsics['fx'], camera_intrinsics['fy'], camera_intrinsics['cx'], camera_intrinsics['cy']
    
    # Transform point cloud to camera frame
    point_cloud_cam = np.dot(rotation_matrix, point_cloud.T).T + translation_vector
    
    # Project points to image plane
    points_2d = np.dot(point_cloud_cam, np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]]).T)
    points_2d = points_2d[:, :2] / points_2d[:, 2][:, np.newaxis]  # divide by z to get (u, v)

    return points_2d.astype(int)

# Load actual point cloud data
point_cloud = o3d.io.read_point_cloud('synthetic_cave.pcd')
point_cloud = np.asarray(point_cloud.points)

# Load RGB image
rgb_image = cv2.imread('synthetic_cave.jpg')

# Project point cloud onto image plane
points_2d = project_point_cloud_to_image(point_cloud, rotation_matrix, translation_vector, camera_intrinsics)

# Create colored point cloud
colored_point_cloud = []
for i, (x, y, z) in enumerate(point_cloud):
    u, v = points_2d[i]
    if 0 <= u < rgb_image.shape[1] and 0 <= v < rgb_image.shape[0]:
        color = rgb_image[v, u, :]
        colored_point_cloud.append([x, y, z, color[2]/255.0, color[1]/255.0, color[0]/255.0])  # Open3D uses float colors

colored_point_cloud = np.array(colored_point_cloud)

# Create Open3D point cloud object
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(colored_point_cloud[:, :3])
pcd.colors = o3d.utility.Vector3dVector(colored_point_cloud[:, 3:])

# Visualize
o3d.visualization.draw_geometries([pcd])
