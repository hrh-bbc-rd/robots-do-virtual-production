from photonlibpy import PhotonCamera, PhotonPoseEstimator, PoseStrategy
from robotpy_apriltag import AprilTagField, AprilTagFieldLayout
import wpimath.geometry
import ntcore
import logging
import time

logging.basicConfig(level=logging.DEBUG)

# Create a NetworkTables instance and start a client
inst = ntcore.NetworkTableInstance.getDefault()
inst.startClient4("photonvision-client")  # Start NT4 client with a name
inst.setServer("127.0.0.1", ntcore.NetworkTableInstance.kDefaultPort4)


# Load the field layout
json_path = "listeningroom_photonvision.json"
try:
    layout = AprilTagFieldLayout(json_path)
except Exception as e:
    print(f"Failed to load field layout: {e}")
    layout = None

# Define the camera name as in the PV UI
camera_name = "USB_Capture_SDI"

# Initialise the PhotonCamera object with the specified camera name
camera = PhotonCamera(camera_name)
time.sleep(1)  # Wait for the camera to initialize

# Define the transform from the robot to the camera
kRobotToCam = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(0.0, 0.0, 0.0),  # x, y, z in meters
    wpimath.geometry.Rotation3d.fromDegrees(0.0, 0.0, 0.0),  # roll, pitch, yaw degrees
)

# Create a PhotonPoseEstimator for estimating the robot's pose using AprilTags
pose_estimator = PhotonPoseEstimator(
    fieldTags=layout,
    strategy=PoseStrategy.MULTI_TAG_PNP_ON_COPROCESSOR,
    camera=camera,
    robotToCamera=kRobotToCam,
)

for i in range(10):  # Loop to repeatedly update the pose estimation
    time.sleep(0.5)  # Wait for 0.5 seconds between updates
    camEstPose = pose_estimator.update()  # Update the pose estimation
    # Print the estimated pose (may be None if no pose is found)
    if camEstPose is not None:
        print(
            f"t = {camEstPose.timestampSeconds}. Estimated pose = {camEstPose.estimatedPose}"
        )
    else:
        print("No pose estimate available.")