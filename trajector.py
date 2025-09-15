import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

bbox_set = pd.read_csv('dataset/bbox_light.csv')

# Compute bounding box center coordinates:
bbox_set['u'] = (bbox_set['x1'] + bbox_set['x2']) / 2
bbox_set['v'] = (bbox_set['y1'] + bbox_set['y2']) / 2
bbox_set_centers = bbox_set[['u', 'v']].values
bbox_set_centers = bbox_set_centers.astype(int)

# Initialize frame 1 first
xyz0 = np.load('dataset/xyz/depth000001.npz')['xyz'] # Shape (H, W, 3) at frame 1
u0, v0 = bbox_set_centers[0] # Traffic light center in frame 1 
point0 = xyz0[v0, u0] # 3d position in traffic light coords
X0, Y0, Z0 = point0[:3]

# Begin full trajectory:
N = 298 # Number of frames
trajectory = np.zeros((N, 2))  # Initialize trajectory array wherein trajectory[i] = [x_forward, y_lateral] at frame i
trajectory[0] = [0, 0]
for i in range(1, N): # Iterate through frames to fill trajectory points
    xyz = np.load(f'dataset/xyz/depth{i+1:06d}.npz')['xyz']
    u, v = bbox_set_centers[i] # Traffic light center in frame i+1
    point = xyz[v, u][:3] # 3d position in traffic light coords
    if np.any(np.isnan(point)) or np.all(point == 0):
        trajectory[i] = trajectory[i - 1]  # Keep previous position if bad point (noise handling)
    else:
        X, Y, Z = point
        trajectory[i] = [X - X0, Y - Y0]  # Relative to initial traffic light position

# Plot it! trajectory.png
plt.figure(figsize=(10, 6))
plt.scatter(trajectory[:, 0], trajectory[:, 1], marker='o', s=20, linewidths=1, label='Ego Trajectory')
plt.scatter(trajectory[-1, 0], trajectory[-1, 1], color='red', marker='x', s=100, label='Start')
plt.scatter(trajectory[0, 0], trajectory[0, 1], color='green', marker='o', s=100, label='End')
plt.scatter(0, 0, color='black', marker='*', s=150, label='Traffic light (origin)')
plt.text(0.5, 0.5, 'Origin', fontsize=12, color='black')
plt.title('Ego Trajectory')
plt.xlabel('Forward (X, m)')
plt.ylabel('Lateral (Y, m)')
plt.grid(True)
plt.xlim(-30, 30)
plt.ylim(-20, 20)
plt.legend()
plt.savefig('trajectory.png', dpi=200)


# Animate it! trajectory.mp4
N = trajectory.shape[0]
fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot([], [], color='blue', linewidth=2, label='Ego Trajectory')
current = ax.scatter([], [], color='orange', s=100, label='Current Position')
start = ax.scatter([], [], color='red', marker='x', s=100, label='Start')
end = ax.scatter([], [], color='green', marker='o', s=100, label='End')
origin = ax.scatter(0, 0, color='black', marker='*', s=150, label='Traffic light (origin)')
ax.text(0.5, 0.5, 'Origin', fontsize=12, color='black')
ax.set_xlim(-30, 30)
ax.set_ylim(-20, 20)
ax.set_xlabel('Forward (X, m)')
ax.set_ylabel('Lateral (Y, m)')
ax.set_title('Animated Ego Trajectory')
ax.grid(True)
ax.set_xlim(-30, 30)
ax.set_ylim(-20, 20)
ax.legend()

frame_text = ax.text(-28, 19, '', fontsize=12, color='gray')

def update(frame):
    line.set_data(trajectory[-frame:, 0], trajectory[-frame:, 1])  # Line buildup
    current.set_offsets([trajectory[-frame]]) # Current position
    frame_text.set_text(f'Frame: {frame}')
    return line, current, start, end, frame_text


start.set_offsets([trajectory[-1]])   
end.set_offsets([trajectory[0]])   
ani = FuncAnimation(fig, update, frames=range(N), interval=50, blit=True)
plt.rcParams['animation.ffmpeg_path'] = r'C:\Users\richa\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-full_build\bin\ffmpeg.exe'
writer = FFMpegWriter(fps=20, bitrate=500)
ani.save('trajectory.mp4', writer=writer, dpi=200)
