import requests
import os

import mars2020

mars = mars2020.Mars2020()

images, query = mars.get_data(sort="newest")

outputdir = "./images"

for image in images:
    *_, basename = image.image_fullres.split("/")
    filename, ext = basename.split(".")

    image_req = requests.get(image.image_fullres)

    dirname = os.path.join(outputdir, str(image.sol))
    full_path_file = os.path.join(dirname, basename)

    os.makedirs(dirname, exist_ok=True)

    with open(full_path_file, 'wb') as f:
        print(f"downloading to {full_path_file}")
        f.write(image_req.content)
