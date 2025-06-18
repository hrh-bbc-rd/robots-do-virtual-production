from photonlibpy import PhotonCamera, PhotonPoseEstimator, PoseStrategy
from robotpy_apriltag import AprilTagField, AprilTagFieldLayout
import wpimath.geometry
import ntcore
import logging
import time
import random
logging.basicConfig(level=logging.DEBUG)

# Create a NetworkTables instance and start a client
inst = ntcore.NetworkTableInstance.getDefault()
inst.startClient4("photonvision-client")  # start NT4 client with a name
inst.setServer("127.0.0.1", ntcore.NetworkTableInstance.kDefaultPort4)

camera_name = 'USB_Capture_SDI' #'VirtualBox_Webcam_-_OBS_Virtual_Camera'

# Initialise camera
camera = PhotonCamera(camera_name)
time.sleep(5)


kRobotToCam = wpimath.geometry.Transform3d(
    wpimath.geometry.Translation3d(0.5, 0.0, 0.5),
    wpimath.geometry.Rotation3d.fromDegrees(0.0, -30.0, 0.0),
)


camPoseEst = PhotonPoseEstimator(
    AprilTagFieldLayout.loadField(AprilTagField.kDefaultField),
    PoseStrategy.LOWEST_AMBIGUITY,
    camera,
    kRobotToCam,
)

camEstPose = camPoseEst.update()
print(camEstPose.estimatedPose)