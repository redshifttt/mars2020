import json
import requests
import sys
import os
import math
import datetime
from dataclasses import dataclass

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
    # =========
    "HELI_NAV": "Ingenuity Navigation Camera",
    "HELI_RTE": "Ingenuity Color Camera",
}

@dataclass
class Image:
    sol: int
    attitude: tuple[float]
    caption: str
    sample_type: str
    date_taken_mars: str
    credit: str
    date_taken_utc: datetime.datetime
    link: str
    drive: int
    title: str
    site: int
    date_received: datetime.datetime

    mast_azimuth: float
    mast_elevation: float
    sclk: float # no idea what this is
    scale_factor: int
    xyz: tuple[float]
    subframe_rect: tuple[int]
    dimension: tuple[int]

    image_small: str
    image_medium: str
    image_large: str
    image_fullres: str

    camera_filter_name: str
    camera_vector: tuple[float]
    camera_model_component_list: str
    camera_position: tuple[float]
    instrument: str
    camera_model_type: str

@dataclass
class QueryResults:
    total_results: int
    total_images: int

class Mars2020:
    def __init__(self):
        pass

    def get_data(self, results=100, page=1, cameras=["MCZ_LEFT", "MCZ_RIGHT"], sort="newest"):
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

        # I like to err on the side of.. well no error handling I guess... what's the worst that could happen?
        api_req = requests.get(f"https://mars.nasa.gov/rss/api/?feed=raw_images&category=mars2020,ingenuity&feedtype=json&ver=1.2&num={results}&page={page}&order={sort}&search={joined_cameras}&")
        api_res = json.loads(api_req.text)

        total_results = api_res["total_results"]
        total_images = api_res["total_images"]

        images = []

        for image in api_res["images"]:
            attitude = tuple(image["attitude"].strip("()").split(","))
            date_taken_utc = datetime.datetime.fromisoformat(image["date_taken_utc"])
            date_received = datetime.datetime.fromisoformat(image["date_received"])
            drive = image["drive"]
            sol = image["sol"]
            caption = image["caption"]
            sample_type = image["sample_type"]
            date_taken_mars = image["date_taken_mars"]
            credit = image["credit"]
            link = image["link"]
            title = image["title"]
            site = image["site"]

            mast_azimuth = image["extended"]["mastAz"]
            mast_elevation = image["extended"]["mastEl"]
            sclk = image["extended"]["sclk"]
            scale_factor = int(image["extended"]["scaleFactor"])
            xyz = image["extended"]["xyz"]
            subframe_rect = tuple(image["extended"]["subframeRect"].strip("()").split(","))
            dimension = tuple(image["extended"]["dimension"].strip("()").split(","))

            image_small = image["image_files"]["small"]
            image_medium = image["image_files"]["medium"]
            image_large = image["image_files"]["large"]
            image_fullres = image["image_files"]["full_res"]

            camera_filter_name = image["camera"]["filter_name"]
            camera_vector = tuple(image["camera"]["camera_vector"].strip("()").split(","))
            camera_model_component_list = image["camera"]["camera_model_component_list"]
            camera_position = tuple(image["camera"]["camera_position"].strip("()").split(","))
            instrument = image["camera"]["instrument"]
            camera_model_type = image["camera"]["camera_model_type"]

            images.append(Image(
                sol,
                attitude,
                caption,
                sample_type,
                date_taken_mars,
                credit,
                date_taken_utc,
                link,
                drive,
                title,
                site,
                date_received,

                mast_azimuth,
                mast_elevation,
                sclk,
                scale_factor,
                xyz,
                subframe_rect,
                dimension,

                image_small,
                image_medium,
                image_large,
                image_fullres,

                camera_filter_name,
                camera_vector,
                camera_model_component_list,
                camera_position,
                instrument,
                camera_model_type
            ))

        return images, QueryResults(total_results, total_images)
