# MICADO installer

This project is a command-line interface (CLI) application for the MICADO project, built with [Typer](https://typer.tiangolo.com/). It provides functionalities to properly deploy the MICADO platform on a linux based system.

## Features

- **Download GitHub Releases:** Fetch and download release tarballs from the MICADO GitHub repository.
- **File Operations:** Extract tarballs and manage file operations within specified directories.
- **Docker Management:** Execute Docker commands using `docker-compose` files included in the downloaded content.

## Example Commands

### Prepare Command

```sh
micado_install prepare download --release v1.0.0 --path /path/to/install
```
### Configure Command

```sh
micado_install configure environment

OR

micado_install configure environment \
  --postgres-password 'Abcdef1!' \
  --keycloak-admin-password 'Abcdef1!' \
  --identity-hostname id.example.local \
  --migrants-hostname migrants.example.local \
  --pa-hostname pa.example.local \
  --ngo-hostname ngo.example.local \
  --traefik-acme-email admin@example.com \
  --traefik-hostname traefik.example.local \
  --git-hostname git.example.local \
  --gitea-db-password 'Abcdef1!' \
  --gitea-admin-password 'Abcdef1!' \
  --gitea-admin-email admin@example.com \
  --weblate-email-host smtp.example.local \
  --weblate-email-host-user weblate \
  --weblate-server-email weblate@example.local \
  --weblate-default-from-email weblate@example.local \
  --weblate-admin-password 'Abcdef1!' \
  --weblate-admin-email weblate-admin@example.local \
  --translation-hostname translate.example.local \
  --weblate-postgres-password 'Abcdef1!' \
  --timezone 'Europe/Rome' \
  --micado-db-password 'Abcdef1!' \
  --weblate-email-host-password 'Abcdef1!' \
  --algorithm-password 'Abcdef1!' \
  --micado-weblate-key 'abcdef0123456789' \
  --portainer-hostname portainer.example.local \
  --api-hostname api.example.local
```

### Deploy Command

```sh
micado_install deploy --docker-compose /path/to/install/docker-compose.yaml
```

# Usage

## Downloading and Installing the Compiled Program

1. Navigate to the [MICADO installer Releases page](https://github.com/micado-eu/installer/releases) of the repository.
2. Find the latest release tagged with the version you are interested in (e.g., `v1.0.0`).
3. Download the `micado_install` executable file from the release assets.

#### Install the Compiled Program

1. Ensure the downloaded file (`micado_install`) has executable permissions. On Unix-like systems, you can do this with the following command:
    ```sh
    chmod +x micado_install
    ```

2. Move the executable to a directory that is in your system's `PATH` (optional but recommended for easy access). For example:
    ```sh
    sudo mv micado_install /usr/local/bin/
    ```

3. Verify the installation by running the executable:
    ```sh
    micado_install --help
    ```


## Prepare Application

To prepare the MICADO application for a specific release, use the following command:

```bash
micado_install prepare download --release <RELEASE> --path <PATH>
```

- `--release`: The release version to prepare (e.g., `v1.0.0`).
- `--path`: The path where the MICADO application will be installed.


## Configure Environment

To configure the environment for the MICADO application, use the following command:

```bash
micado_install configure environment
```

This command will prompt you for various environment variables, validate them, and create the necessary folders. Here are the parameters you will be prompted for:

- PostgreSQL password
- Keycloak admin password
- Keycloak identity hostname
- Migrants application hostname
- Public Administration application hostname
- NGO application hostname
- Analytics application hostname
- Traefik ACME email
- Traefik hostname
- Gitea Git server hostname
- Gitea database password
- Weblate email host
- Weblate email host user
- Weblate server email
- Weblate default from email
- Weblate admin password
- Weblate admin email
- Translation platform hostname
- Weblate PostgreSQL password
- Timezone
- MICADO database password
- Weblate email host password
- Algorithm password
- MICADO Weblate key
- Portainer hostname

### Deploy Application

To deploy the MICADO application using Docker Compose, use the following command:

```bash
micado_install deploy compose-up
```

This command checks if the environment is prepared by verifying the presence of necessary files and directories, then it runs `docker-compose up -d`.

### Finalize the deployment
Some components require some additional operation that can be done only after that the service are started.
To do this you will need to execute:

``` bash
micao_install deploy finalize-deployment
```

### Stop and Remove Application

To stop and remove the MICADO application using Docker Compose, use the following command:

```bash
micado_install deploy compose-down
```

This command stops and removes the MICADO application using `docker-compose down`.

### Example Usage

1. **Prepare the Application:**

   ```bash
   micado_install prepare download --release v1.0.0 --path /path/to/install
   ```

2. **Configure the Environment:**

   ```bash
   micado_install configure environment
   ```

3. **Deploy the Application:**

   ```bash
   micado_install deploy compose-up
   ```

4. **Stop and Remove the Application:**

   ```bash
   micado_install deploy compose-down
   ```

# Development
To develop the MICADO installer there is a Dockerfile to execute the application in a containerized environment.

## Image preparation
In case of the need to use new python libraries is necessary to create a new development library
```
docker build -t micadoproject/installer .
```

## Testing commands
This is the command to execute to run the installer in development
```
docker run -v $PWD:/usr/src/app -it --rm  --user <user> micadoproject/installer python main.py
```

## Development workflow
To code the installer, use the following workflow:
```
docker run -v $PWD:/usr/src/app -v /var/run/docker.sock:/var/run/docker.sock -it --rm  python:3.9.10 /bin/bash
cd /usr/src/app
pip3 install -r requirements.txt
python main.py prepare prepare
```

This will allow for a consistent development environment where the code is executed.


## Project Structure

```
micado_installer/
│
├── Dockerfile
├── main.py
├── README.md
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── prepare.py
│   │   ├── configure.py
│   │   ├── deploy.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── checks.py
│   │   ├── fileops.py
│   │   ├── git.py
│
├── tests/
│   ├── __init__.py
│   ├── test_prepare.py
│   ├── README.md
```

### Folder Structure

- **Dockerfile**: Defines the Docker container for the application. Used in the development phase to ensure the development environment is always consistent and coherent.
- **main.py**: The main entry point for the Typer CLI application.
- **README.md**: Project documentation.
- **requirements.txt**: File listing the project dependencies.
- **app/**: Contains the main application code.
  - **commands/**: Contains CLI command definitions.
    - `prepare.py`: Handles downloading and unzipping GitHub releases.
    - `configure.py`: Manages the configuration of the unzipped content.
    - `deploy.py`: Executes Docker commands using the `docker-compose.yaml` file from the unzipped content.
  - **core/**: Contains core application code such as configuration, database setup, and security.
    - `checks.py`: Implements various checks used by the application.
    - `fileops.py`: Includes file operations like moving to the install folder, extracting tarballs, and deleting files.
    - `git.py`: Contains functions to interact with GitHub releases, including fetching releases and downloading tarballs.
- **tests/**: Contains unit tests for the application.
  - `test_prepare.py`: Tests for the `prepare` command.
  - `README.md`: Documentation for the tests.

## Development

### Image Preparation
To ensure a coherent development envuronment the Dockerfile provides a containerized envuronment where developing the code.
In case of the need to use new Python libraries, it is necessary to create a new development image:

```sh
docker build -t micadoproject/installer .
```

### Running the Installer in Development

To run the installer in development, use the following Docker command to execute the prepared Docker image and code inside the created container for a coherent coding environment:

1. Run the Docker container and mount the current directory:

    ```sh
    docker run -v $PWD:/usr/src/app -v /var/run/docker.sock:/var/run/docker.sock -it --rm python:3.9.10 /bin/bash
    ```

2. Inside the container, navigate to the application directory:

    ```sh
    cd /usr/src/app
    ```

3. Install the required Python libraries:

    ```sh
    pip3 install -r requirements.txt
    ```

4. Run the installer:

    ```sh
    python main.py prepare
    ```

### Adding New Commands

To add a new command:

1. Create a new Python file in the `app/commands` directory.
2. Define the command using the `@app.command()` decorator from Typer.
3. Implement the required functionality.
4. Update this `README.md` file with details about the new command.

### Running Tests

Run tests using `pytest` to ensure the commands work as expected:

```sh
pytest tests/
```

## GitHub Actions Workflow Description

The goal of this automation is to simplify and streamline the process of generating an executable file for the Micado project. Each time the project’s main branches are updated or a new version is tagged, the system automatically compiles the Python code into a standalone executable file. This means that non-technical users can easily install and run the software without needing to deal with the source code or manual setup. By automating the creation of the executable, this approach saves time, ensures consistency, and reduces errors, allowing developers to focus on improving the project while the system handles the technical work of packaging the software for release.

### Workflow Overview

This project uses GitHub Actions to automate the build and release process. The workflow is defined in `.github/workflows/main.yaml` and performs the following steps:

1. **Checkout Repository**: Clones the repository's code to the GitHub runner.
2. **Build Executable**: Uses PyInstaller to create a standalone executable from the Python code.
3. **Generate Release Tag**: Creates the next release tag.
4. **Create Release**: Uploads the executable artifact to a new release on GitHub.

The workflow is named "Build Installer" and is triggered on specific events:

- When code is pushed to the `master` or `2024` branches.
- When a tag matching the pattern `v*` is pushed.

#### Workflow Steps

1. **Checkout Repository**:
   - Uses the `actions/checkout@v4` action to clone the repository's code to the GitHub runner.

2. **Build Executable**:
   - Uses the `sayyid5416/pyinstaller@v1` action to build a standalone executable from the Python code.
   - The action is configured with:
     - `python_ver`: The Python version to use (3.9).
     - `spec`: The entry point for the application (`main.py`).
     - `requirements`: The requirements file listing the dependencies (`requirements.txt`).
     - `options`: PyInstaller options (`--onefile`, `--name "micado_install"`).

3. **Generate Release Tag**:
   - Uses the `alexvingg/next-release-tag@v1.0.4` action to generate the next release tag.
   - The GitHub token is used for authentication, and no specific tag prefix is used.

4. **Create Release**:
   - Uses the `ncipollo/release-action@v1` action to create a new release on GitHub.
   - The executable artifact (`micado_install`) is uploaded to the release.
   - The release includes:
     - A body message ("Release of Micado Installer").
     - The generated release tag.



## Contribution

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License.


