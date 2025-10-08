from photonlibpy import PhotonCamera
import ntcore
import logging
import time
import json

logging.basicConfig(level=logging.DEBUG)


def setup_networktables(server="127.0.0.1", client_name="photonvision-client"):
    inst = ntcore.NetworkTableInstance.getDefault()
    inst.startClient4(client_name)
    inst.setServer(server, ntcore.NetworkTableInstance.kDefaultPort4)
    return inst


def setup_camera(camera_name):
    camera = PhotonCamera(camera_name)
    time.sleep(3)  # Wait for the camera to initialize
    return camera


def extract_tags(camera):
    tags = camera.getLatestResult().getTargets()
    tag_list = []
    for tag in tags:
        i = tag.fiducialId
        q = tag.bestCameraToTarget.rotation().getQuaternion()
        x = tag.bestCameraToTarget.translation()
        tag_list.append(
            {
                "ID": int(i),
                "pose": {
                    "translation": {
                        "x": x.X(),
                        "y": x.Y(),
                        "z": x.Z(),
                    },
                    "rotation": {
                        "quaternion": {
                            "W": q.W(),
                            "X": q.X(),
                            "Y": q.Y(),
                            "Z": q.Z(),
                        }
                    },
                },
            }
        )
    return tag_list


def load_existing_json(output_file):
    try:
        with open(output_file, "r") as f:
            existing_data = json.load(f)
            print(f"Adding to existing: {output_file}")
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {"tags": [], "field": {"length": 0.0, "width": 0.0}}
        print(f"Creating new file: {output_file}")
    return existing_data


def update_json_with_tags(existing_data, new_tags):
    existing_tag_ids = {tag["ID"] for tag in existing_data.get("tags", [])}
    print(f"Existing tags are {existing_tag_ids}")
    for tag in new_tags:
        if tag["ID"] not in existing_tag_ids:
            existing_data["tags"].append(tag)
    tag_ids = [tag["ID"] for tag in existing_data.get("tags", [])]
    print(f"New list of tags in json {tag_ids}")
    return existing_data


def save_json(output_file, data):
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print(f"Wrote {output_file}")


def main(camera_name="USB_Capture_SDI", output_file="lr_singletag_map.json"):
    setup_networktables()
    camera = setup_camera(camera_name)
    tags = extract_tags(camera)
    json_data = {"tags": tags, "field": {"length": 0.0, "width": 0.0}}
    existing_data = load_existing_json(output_file)
    # Optionally update field info if needed
    existing_data["field"] = json_data.get("field", existing_data.get("field", {}))
    updated_data = update_json_with_tags(existing_data, tags)
    save_json(output_file, updated_data)


if __name__ == "__main__":
    main()
