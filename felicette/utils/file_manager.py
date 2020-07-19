import tempfile
import os
import requests
from tqdm import tqdm

from felicette.constants import band_tag_map

workdir = os.path.join(os.path.expanduser("~"), "felicette-data")

def check_sat_path(id):
    data_path = os.path.join(workdir, id)

    if not os.path.exists(data_path):
        os.mkdir(data_path)


def save_to_file(url, filename, id):
    data_path = os.path.join(workdir, id)
    data_id = filename.split("-")[1].split(".")[0]
    print("Downloading %s band" % band_tag_map[data_id])
    file_path = os.path.join(data_path, filename)
    response = requests.get(url, stream=True)
    with tqdm.wrapattr(
        open(file_path, "wb"),
        "write",
        miniters=1,
        desc=filename,
        total=int(response.headers.get("content-length", 0)),
    ) as fout:
        for chunk in response.iter_content(chunk_size=4096):
            fout.write(chunk)
    fout.close()


def data_file_exists(filename, id):
    data_path = os.path.join(workdir, id)
    file_path = os.path.join(data_path, filename)
    return os.path.exists(file_path)


def file_paths_wrt_id(id):
    home_path_id = os.path.join(workdir, id)
    return {
        "base": home_path_id,
        "b4": os.path.join(home_path_id, "%s-b4.tiff" % (id)),
        "b3": os.path.join(home_path_id, "%s-b3.tiff" % (id)),
        "b2": os.path.join(home_path_id, "%s-b2.tiff" % (id)),
        "b8": os.path.join(home_path_id, "%s-b8.tiff" % (id)),
        "stack": os.path.join(home_path_id, "%s-stack.tiff" % (id)),
        "pan_sharpened": os.path.join(home_path_id, "%s-pan.tiff" % (id)),
        "output_path": os.path.join(home_path_id, "%s-color-processed.tiff" % (id)),
        "output_path_jpeg": os.path.join(
            home_path_id, "%s-color-processed.jpeg" % (id)
        ),
    }
