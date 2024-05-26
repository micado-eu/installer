# Testing Code Explanation

## Prepare Overview

This test suite is designed to test the `prepare` command of a Typer CLI application. The tests are written using `pytest` and `typer.testing.CliRunner`. Mocking is employed to simulate interactions with external systems and file operations.

### Test File Structure

- **Fixtures**:
  - `mock_get_github_releases_enum`
  - `mock_file_operations`
  - `valid_directory`
- **Tests**:
  - `test_prepare_command`
  - `test_prepare_command_invalid_path`

### Fixtures

#### `mock_get_github_releases_enum`

This fixture mocks the `get_github_releases_enum` function from the `app.core.git` module.

```python
@pytest.fixture
def mock_get_github_releases_enum(monkeypatch):
    def mock_releases_enum(owner, repo):
        return [("v1_0", "v1.0"), ("v2_0", "v2.0")]
    monkeypatch.setattr(git, "get_github_releases_enum", mock_releases_enum)
```

- **Purpose**: Simulates fetching GitHub releases by returning a predefined list of release names and values.
- **Implementation**: Uses `monkeypatch` to replace the actual function with a mock function.

#### `mock_file_operations`

This fixture mocks various file operations functions from `app.core.fileops` and `app.core.git`.

```python
@pytest.fixture
def mock_file_operations(monkeypatch):
    def mock_move_to_install_folder(path):
        pass
    def mock_download_release_tarball(owner, repo, release):
        return "/path/to/tarball.tar.gz"
    def mock_extract_tarball(tarball_path):
        pass
    def mock_delete_file(tarball_path):
        pass

    monkeypatch.setattr(fileops, "move_to_install_folder", mock_move_to_install_folder)
    monkeypatch.setattr(git, "download_release_tarball", mock_download_release_tarball)
    monkeypatch.setattr(fileops, "extract_tarball", mock_extract_tarball)
    monkeypatch.setattr(fileops, "delete_file", mock_delete_file)
```

- **Purpose**: Simulates file operations without actually performing them.
- **Functions Mocked**:
  - `move_to_install_folder`
  - `download_release_tarball`
  - `extract_tarball`
  - `delete_file`

#### `valid_directory`

This fixture provides a valid temporary directory for testing.

```python
@pytest.fixture
def valid_directory(tmp_path):
    return tmp_path
```

- **Purpose**: Ensures the tests use a valid directory path.

### Tests

#### `test_prepare_command`

Tests the `prepare` command with valid inputs.

```python
def test_prepare_command(mock_get_github_releases_enum, mock_file_operations, valid_directory):
    result = runner.invoke(app, ["prepare", "--release", "v1_0", "--path", str(valid_directory)])
    assert result.exit_code == 0
    assert "Preparing MICADO application' folders" in result.output
```

- **Steps**:
  - Uses `CliRunner` to invoke the `prepare` command with valid release and path.
  - Asserts that the command exits with code `0`.
  - Checks if the expected output message is printed.

#### `test_prepare_command_invalid_path`

Tests the `prepare` command with an invalid path.

```python
def test_prepare_command_invalid_path(mock_get_github_releases_enum):
    invalid_path = "/invalid/path"
    result = runner.invoke(app, ["prepare", "--release", "v1_0", "--path", invalid_path])
    assert result.exit_code != 0
    assert f"The path {invalid_path} you indicated do not exists!" in result.output
```

- **Steps**:
  - Uses `CliRunner` to invoke the `prepare` command with a valid release but an invalid path.
  - Asserts that the command does not exit with code `0`.
  - Checks if the appropriate error message is printed.

### Running the Tests

Ensure you have `pytest` and `typer` installed:

```sh
pip install pytest typer
```

Run the tests using:

```sh
pytest
```

### Summary

- **Fixtures**: Mock external dependencies and provide necessary setup.
- **Tests**: Validate the `prepare` command functionality and error handling.
- **Tools**: `pytest` for testing and `typer.testing.CliRunner` for command-line interface testing.

This setup ensures that the `prepare` command works correctly without performing real HTTP requests or file operations during testing.

