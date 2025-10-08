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


def add_tag_to_json(i, Q, T):
    """
    Adds tag information to the json_data["tags"] list.

    Args:
        i: Tag ID (int)
        Q: Rotation as a quaternion
        T: Translation
    """
    json_data["tags"].append(
        {
            "ID": int(i),
            "pose": {
                "translation": {
                    "x": T.X(),
                    "y": T.Y(),
                    "z": T.Z(),
                },
                "rotation": {
                    "quaternion": {
                        "W": Q.W(),
                        "X": Q.X(),
                        "Y": Q.Y(),
                        "Z": Q.Z(),
                    }
                },
            },
        }
    )


# Get the latest detected AprilTag targets from the camera
tags = camera.getLatestResult().getTargets()

for tag in tags:
    i = tag.fiducialId  # Tag ID
    q = tag.bestCameraToTarget.rotation().getQuaternion()
    x = tag.bestCameraToTarget.translation()
    add_tag_to_json(i, q, x)  # Add tag info to the JSON data

# Only add new tag entries that are not already present in the JSON file
output_file = "lr_singletag_map.json"

# Load existing data if file exists
try:
    with open(output_file, "r") as f:
        existing_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    existing_data = {"tags": [], "field": {"length": 0.0, "width": 0.0}}

# Build a set of existing tag IDs for quick lookup
existing_tag_ids = {tag["ID"] for tag in existing_data.get("tags", [])}

# Add only new tags from json_data
for tag in json_data["tags"]:
    if tag["ID"] not in existing_tag_ids:
        existing_data["tags"].append(tag)

# Optionally update field info if needed
existing_data["field"] = json_data.get("field", existing_data.get("field", {}))

with open(output_file, "w") as f:
    json.dump(existing_data, f, indent=2)
    f.write("\n")
