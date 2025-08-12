import requests

micado_release_file = "micado_deployment_"

def get_github_releases_enum(owner, repo, exclude_releases=None):
    """
    Retrieves a list of GitHub releases for a given repository, excluding any releases specified in the `exclude_releases` list.

    Args:
        owner (str): The GitHub username or organization name that owns the repository.
        repo (str): The name of the repository.
        exclude_releases (list, optional): A list of release names to exclude from the returned list. Defaults to an empty list.

    Returns:
        list: A list of tuples, where each tuple contains the release name and the release name.
    """
    if exclude_releases is None:
        exclude_releases = []

    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    response = requests.get(url)
    if response.status_code == 200:
        releases = response.json()
        release_enum = []
        for release in releases:
            if release["name"] not in exclude_releases:
                # Add each release name to the enumeration
                release_enum.append((release["name"], release["name"]))
        return release_enum
    else:
        print("Failed to fetch releases. Status code:", response.status_code)
        return []


def download_release_tarball(owner, repo, release_name):
    """
    Downloads the release tarball for the specified GitHub repository and release name.

    Args:
        owner (str): The GitHub username or organization name that owns the repository.
        repo (str): The name of the GitHub repository.
        release_name (str): The name of the GitHub release to download.

    Returns:
        str: The path to the downloaded tarball file, or `None` if the download failed.
    """
    print(f"Downloading tarball for release {release_name}...")
    # TODO remove this line once the release is ready
    # release_name = "2.0.0"  # Replace with the name of the release 2.0.0 for testing
    url = f"https://github.com/{owner}/{repo}/releases/download/{release_name}/{micado_release_file}{release_name}.tar.gz"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        # Save the tarball to a file
        with open(f"{micado_release_file}{release_name}.tar.gz", "wb") as f:
            f.write(response.content)
        print(f"Tarball for release {release_name} downloaded successfully.")
        return f"{micado_release_file}{release_name}.tar.gz"
    else:
        print(
            f"Failed to download tarball for release {release_name}. Status code:",
            response.status_code,
        )
        return None

