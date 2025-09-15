# Perception Coding Challenge 
Richard Li

## Methodology - trajector.py

- Get the center pixel values at every frame of the bounding box for the traffic light
- I initialized frame 1 first for clarity as a starting point, which allows me to use the offset values for ground frame view.
- I then iterated through every frame while ignoring noise/NAN/0,0,0 items at O(n) with frames in reverse order
- Used matplotlib to graph and animate

## Assumptions

- Machine Learning/CV not required
- World/ground frame (BEV) sets traffic light at origin
- Camera coord system (X forward, Y right axis, Z upward)
- Right-handed coord system for ground frame (X forward, Y left, Z upward)

## Results - trajectory.png, trajectory.mp4

- trajectory.png with a curve that begins somewhere around -27,16 and ends at 0,0 (all meters) computed at O(n) 
- trajectory.mp4 to animate the pathway taken by the vehicle computed at O(n^2)
- Mapped out traffic light and ego only
