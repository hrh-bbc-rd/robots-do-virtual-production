from photonlibpy import PhotonCamera, PhotonPoseEstimator, PoseStrategy
from robotpy_apriltag import AprilTagFieldLayout
import wpimath.geometry
import ntcore
import logging
import time
import socket

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

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 6666  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server is listening...")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            camEstPose = pose_estimator.update()  # Update the pose estimation
            data = f"[{camEstPose.timestampSeconds},{camEstPose.estimatedPose}]"
            if not data:
                break
            conn.sendall(data.encode())
            print("Sent to client")
            time.sleep(1)