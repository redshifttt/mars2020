import json
import requests
import sys
import os
import math

camera_kinds = {
    # Perseverance
    # ============

    # Engineering Cameras
    "NAVCAM_LEFT": "Navigation Camera - Left",
    "NAVCAM_RIGHT": "Navigation Camera - Right",
    "FRONT_HAZCAM_LEFT_A|FRONT_HAZCAM_LEFT_B": "Front Hazcam - Left",
    "FRONT_HAZCAM_RIGHT_A|FRONT_HAZCAM_LEFT_B": "Front Hazcam - Right",
    "REAR_HAZCAM_LEFT": "Rear Hazcam - Left",
    "REAR_HAZCAM_RIGHT": "Rear Hazcam - Right",
    "CACHECAM": "Sample Caching System (CacheCam)",

    # Science Cameras
    "MCZ_LEFT": "Mastcam-Z - Left",
    "MCZ_RIGHT": "Mastcam-Z - Right",
    "SKYCAM": "MEDA SkyCam",
    "PIXL_MCC": "PIXL Micro Context Camera",
    "SHERLOC_WATSON": "SHERLOC - WATSON",
    "SHERLOC_ACI": "SHERLOC Context Imager",
    "SUPERCAM_RMI": "SuperCam Remote Micro Imager",

    # Entry, Descent and Landing Cameras
    "EDL_PUCAM1": "Parachute Up-Look Camera A",
    "EDL_PUCAM2": "Parachute Up-Look Camera B",
    "EDL_DDCAM": "Descent Stage Down-Look Camera",
    "EDL_RUCAM": "Rover Up-Look Camera",
    "EDL_RDCAM": "Rover Down-Look Camera",
    "LCAM": "Lander Vision System Camera",

    # Ingenuity
    "HELI_NAV": "Ingenuity Navigation Camera",
    "HELI_RTE": "Ingenuity Color Camera",
}

class Mars2020:
    def __init__(self):
        pass

    def download_images(self, results=100, page=1, cameras=["MCZ_LEFT", "MCZ_RIGHT"], sort="newest", outputdir="./images", metadata=False):
        page = page - 1

        for c in cameras:
            if not c in camera_kinds.keys():
                print(f"error: camera '{c}' not found.")
                sys.exit(1)

        if results > 100 or results < 1:
            print(f"error: number of results must be either 1, 100 or somewhere in between.")
            sys.exit(1)

        if sort == "newest":
            sort = "sol+desc"
        else:
            sort = "sol+asc"

        joined_cameras = "|".join(cameras)

        req = requests.get(f"https://mars.nasa.gov/rss/api/?feed=raw_images&category=mars2020,ingenuity&feedtype=json&ver=1.2&num={results}&page={page}&order={sort}&search={joined_cameras}&")

        res = json.loads(req.text)

        total_cam_results = res["total_results"]
        total_pages = math.floor(total_cam_results / results) + 1

        print("Camera(s):", ", ".join([camera_kinds[c] for c in cameras]))
        print(f"Total pages: {total_pages:,}")
        print(f"Total results: {total_cam_results:,}")

        image_urls = []

        for image in res["images"]:
            sol = image["sol"]
            full_res_url = image["image_files"]["full_res"]
            *_, filename = full_res_url.split("/")

            image_urls.append((sol, filename, full_res_url))

        for sol, filename, image_url in image_urls:
            dir_to_make = os.path.join(outputdir, str(sol))
            output_name = os.path.join(dir_to_make, filename)

            os.makedirs(dir_to_make, exist_ok=True)

            response = requests.get(image_url)
            with open(output_name, 'wb') as f:
                print("downloading to", output_name)
                f.write(response.content)

mars2020 = Mars2020()

mars2020.download_images(cameras=["HELI_NAV"])
