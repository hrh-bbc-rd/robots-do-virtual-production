from photonlibpy import PhotonCamera, PhotonPoseEstimator, PoseStrategy
from robotpy_apriltag import AprilTagFieldLayout
import wpimath.geometry
import ntcore
import logging
import time
import socket
import json

logging.basicConfig(level=logging.DEBUG)

# Create a NetworkTables instance and start a client
inst = ntcore.NetworkTableInstance.getDefault()
inst.startClient4("photonvision-client")  # Start NT4 client with a name
inst.setServer("127.0.0.1", ntcore.NetworkTableInstance.kDefaultPort4)


# Define the camera name as in the PV UI
camera_name = "USB_Capture_SDI"

# Initialise the PhotonCamera object with the specified camera name
camera = PhotonCamera(camera_name)
time.sleep(3)  # Wait for the camera to initialize

json_data = {"tags": [], "field": {"length": 0.0, "width": 0.0}}

def append_taginfo(i, Q, T):

    x = T.X()
    y = T.Y()
    z = T.Z()

    q_x = Q.X()
    q_y = Q.Y()
    q_z = Q.Z()
    q_w = Q.W()

    json_data["tags"].append(
        {
            "ID": int(i),
            "pose": {
                "translation": {
                    "x": x,
                    "y": y,
                    "z": z,
                },
                "rotation": {
                    "quaternion": {
                        "W": q_w,
                        "X": q_x,
                        "Y": q_y,
                        "Z": q_z,
                    }
                },
            },
        }
    )

tags= camera.getLatestResult().getTargets()
for tag in tags:
    i = tag.fiducialId
    q=tag.bestCameraToTarget.rotation().getQuaternion()
    x=tag.bestCameraToTarget.translation()
    append_taginfo(i, q, x)
    print(x.Y())



with open(f"lr_singletag_map.json", "w") as f:
    json.dump(json_data, f, indent=2)
    f.write("\n")