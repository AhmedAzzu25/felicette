import click
import sys

from felicette.utils.geo_utils import geocoder_util
from felicette.sat_downloader import download_landsat_data, search_landsat_data
from felicette.sat_processor import process_landsat_data


@click.command()
@click.option(
    "-c",
    "--coordinates",
    nargs=2,
    type=float,
    help="Coordinates in (lon, lat) format. This overrides -l command",
)
@click.option("-l", "--location-name", type=str, help="Location name in string format")
@click.option(
    "-p",
    "--pan-enhancement",
    default=False,
    is_flag=True,
    help="Enhance image with panchromatic band",
)
@click.option(
    "-pre",
    "--preview-image",
    default=False,
    is_flag=True,
    help="Preview pre-processed low resolution RGB satellite image.",
)
def main(coordinates, location_name, pan_enhancement, preview_image):
    """Satellite imagery for dummies."""
    if not coordinates and not location_name:
        click.echo("Please specify either --coordinates or --location-name")
        sys.exit(1)
    if location_name:
        coordinates = geocoder_util(location_name)

    # unless specified, cloud_cover_lt is 10
    landsat_item = search_landsat_data(coordinates, 10)

    # set bands to process
    bands = [2, 3, 4]
    if pan_enhancement:
        bands.append(8)

    # download data
    data_id = download_landsat_data(landsat_item, bands)
    # process data
    process_landsat_data(data_id, bands)


if __name__ == "__main__":
    main()
