# Mars 2020 Raw Images API

Python library for the Mars 2020 (Perseverance rover, Ingenuity helicopter) Raw Images API.

## In the Works

The following is a list of in-the-works features:

- Timestamp-based image saving
- Better formatting options
- `ffmpeg` fun and games
- and more...!

## Examples

Download latest 100 (or whatever you specify) images on the first page:

```python
import requests
import os

import mars2020

mars = Mars2020()

images, query = mars.get_data(sort="newest", results=100)

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
```

See [download_latest_100_images.py](download_latest_100_images.py)
