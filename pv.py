from photonlibpy import PhotonCamera, PhotonPoseEstimator, PoseStrategy
from robotpy_apriltag import AprilTagField, AprilTagFieldLayout
import ntcore
import logging
import time
from pprint import pprint
logging.basicConfig(level=logging.DEBUG)

# Create a NetworkTables instance and start a client
inst = ntcore.NetworkTableInstance.getDefault()
inst.startClient4("photonvision-client")  # start NT4 client with a name
inst.setServer("127.0.0.1", ntcore.NetworkTableInstance.kDefaultPort4)

camera_name = 'Trust_Webcam' #'VirtualBox_Webcam_-_OBS_Virtual_Camera'


# Initialise camera
camera = PhotonCamera(camera_name)
time.sleep(5)


pprint(camera.getLatestResult().getTargets())

# Subscribe to the targetPixelsX topic with a default value of 0.0
# target_pixels_x_sub = camera_table.getDoubleTopic("targetPixelsX").subscribe(0.0)

# for x in range (5):
#     print (target_pixels_x_sub.get())
#     time.sleep(1)




# # Print all data from the camera's table
# camera_table = inst.getTable('photonvision').getSubTable(camera_name)
# print("Camera table keys:", camera_table.getKeys())

# # Check if targets are present according to NetworkTables
# has_target_entry = camera_table.getBoolean("hasTarget", False)
# print(f"NT hasTarget: {has_target_entry}")

# # Try to get targets array directly from NetworkTables
# targets_entry = camera_table.getStringArray("targets", [])
# print(f"NT targets: {targets_entry}")


# # Print all top-level tables
# print("Top-level tables:", inst.getTable("").getSubTables())

# # Look at all entries in the photonvision table
# photon_table = inst.getTable("photonvision")
# print("PhotonVision table entries:", photon_table.getKeys())

# # Check if there's a raw targets entry somewhere else
# for subtable in photon_table.getSubTables():
#     subtable_obj = photon_table.getSubTable(subtable)
#     print(f"{subtable} entries:", subtable_obj.getKeys())

