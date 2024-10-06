import typer

# import requests
from enum import Enum  # , auto
import app.core.git as git
import app.core.fileops as fileops
import os
from typing_extensions import Annotated


app = typer.Typer()


# GitHub repository information
GITHUB_OWNER = "micado-eu"  # Owner of the GitHub repository
GITHUB_REPO = "micado_deployment"  # Repository name

# TODO remove also commented out release, now used as test
# Fetch the releases from GitHub and create Release object dynamically
exclude_list = [
    "MICADO 2.0",
    "MICADO 1.2",
    "MICADO 1.1.9",
    "MICADO 1.1.7",
    "MICADO 1.1.6",
    "MICADO 1.1.5",
    "MICADO 1.1.4",
    "MICADO 1.1.3",
    "MICADO 1.1.2",
    "MICADO 1.1.1",
    "MICADO 1.1",
    "MICADO 1.0.1",
    "MICADO 1.0",
]  # List of releases to exclude
releases = git.get_github_releases_enum(GITHUB_OWNER, GITHUB_REPO, exclude_list)
# The `get_github_releases_enum` function retrieves the list of releases for a specified GitHub repository.
# This list is used to dynamically create an Enum class called Release. Enums provide a way to define a set
# of named values that can be used as constants. In this case, the Release Enum will represent the different
# releases available for the Micado deployment repository.
Release = Enum("Release", releases)  # Creating Release Enum


def path_callback(value: str):
    """
    Validates the path provided as an argument to the `prepare` command.

    This function is used as a callback for the `typer.Option` that prompts the user to enter the path where the MICADO application will be installed. It checks if the provided path is a valid directory, and raises a `typer.BadParameter` exception if the path does not exist.

    Args:
        value (str): The path entered by the user.

    Raises:
        typer.BadParameter: If the provided path does not exist.
    """
    if not os.path.isdir(value):
        raise typer.BadParameter(f"The path {value} you indicated do not exists!")
    return value


@app.command()
def download(
    release: Annotated[Release, typer.Option()],
    path: Annotated[
        str,
        typer.Option(
            prompt="Insert the path where the MICADO application will be installed",
            help="This is the path where the MICADO application will be installed",
            hide_input=True,
            callback=path_callback,
        ),
    ],
):
    """Prepare MICADO installer program.

    This command is used to prepare the MICADO installer program for a specific release. It downloads
    the release tarball from the specified GitHub repository, extracts it, and deletes the tarball file
    after extraction.

    Args:
        release (Release): The release version to prepare.

    """
    print("Preparing MICADO application' folders")

    # Moving to the defined folder to work there
    fileops.move_to_install_folder(path)
    # Downloading release tarball
    tarball_path = git.download_release_tarball(
        GITHUB_OWNER, GITHUB_REPO, release.value
    )
    if tarball_path:
        # Extracting tarball
        fileops.extract_tarball(tarball_path)
        # Deleting tarball
        fileops.delete_file(tarball_path)
