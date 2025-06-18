from photonlibpy import PhotonCamera, PhotonPoseEstimator, PoseStrategy
from robotpy_apriltag import AprilTagField, AprilTagFieldLayout
import wpimath.geometry
import ntcore
import logging
import time
import datetime

# Set up logging to display debug messages
logging.basicConfig(level=logging.DEBUG)

# Create a NetworkTables instance and start a client
inst = ntcore.NetworkTableInstance.getDefault()
inst.startClient4("photonvision-client")  # Start NT4 client with a name
inst.setServer(
    "127.0.0.1", ntcore.NetworkTableInstance.kDefaultPort4)  # Set server address

# Define the camera name as in the PV UI
camera_name = 'USB_Capture_SDI'

# Initialise the PhotonCamera object with the specified camera name
camera = PhotonCamera(camera_name)

time.sleep(5)  # Wait for the camera to initialize

# Define the transform from the robot to the camera (position and orientation)
kRobotToCam = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(0.5, 0.0, 0.5),  # x, y, z translation in meters
    wpimath.geometry.Rotation3d.fromDegrees(
        0.0, -30.0, 0.0),  # roll, pitch, yaw  degrees
)

# Create a PhotonPoseEstimator for estimating the robot's pose using AprilTags
camPoseEst = PhotonPoseEstimator(
    AprilTagFieldLayout.loadField(
        AprilTagField.kDefaultField),  # Load default AprilTag field layout
    PoseStrategy.LOWEST_AMBIGUITY,  # Use pose strategy with lowest ambiguity
    camera,                        # The camera object
    kRobotToCam,                   # The transform from robot to camera
)

# Attempt to update the pose estimation from the camera
camEstPose = camPoseEst.update()

for i in range(10):  # Loop to repeatedly update the pose estimation
    time.sleep(0.1)  # Wait for 0.5 seconds between updates
    camEstPose = camPoseEst.update()  # Update the pose estimation
    # Print the estimated pose (may be None if no pose is found)
    if camEstPose is not None:
        now = datetime.datetime.now().isoformat()
        print(f"Timestamp = {now}. Estimated pose = {camEstPose.estimatedPose}")
    else:
        print("No pose estimate available.")