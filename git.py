import requests

micado_release_file = "micado_deployment_"

def get_github_releases(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    response = requests.get(url)
    if response.status_code == 200:
        releases = response.json()
        return releases
    else:
        print("Failed to fetch releases. Status code:", response.status_code)
        return []

# Replace these with the owner and repository name of the GitHub repository you want to fetch releases for
#owner = "owner_username"
#repo = "repository_name"

#list_github_releases(owner, repo)

def get_github_releases_enum(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    response = requests.get(url)
    if response.status_code == 200:
        releases = response.json()
        release_enum = []
        for release in releases:
            # Add each release name to the enumeration
            release_enum.append((release["name"],release["name"]))
        return release_enum
    else:
        print("Failed to fetch releases. Status code:", response.status_code)
        return []

def download_release_tarball(owner, repo, release_name):
    print(f"Downloading tarball for release {release_name}...")
    # TODO remove this line once the release is ready
    release_name = "2.0.0" # Replace with the name of the release 2.0.0 for testing
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
        print(f"Failed to download tarball for release {release_name}. Status code:", response.status_code)
        return None

