import pytest
from typer.testing import CliRunner
from app.commands.prepare import app
from unittest.mock import patch, MagicMock

runner = CliRunner()

# Mock the functions from the core modules
@patch("app.core.git.download_release_tarball")
@patch("app.core.git.get_github_releases_enum")
@patch("app.core.fileops.move_to_install_folder")
@patch("app.core.fileops.extract_tarball")
@patch("app.core.fileops.delete_file")
def test_download(mock_delete_file, mock_extract_tarball, mock_move_to_install_folder, mock_get_github_releases_enum, mock_download_release_tarball):
    # Mocking the releases enum
    mock_get_github_releases_enum.return_value = [("v1.0.0", "v1_0_0")]

    # Mocking the tarball download
    mock_download_release_tarball.return_value = "/path/to/tarball"

    result = runner.invoke(app, [
        "download",
        "--release", "v1_0_0",
        "--path", "/fake/path"
    ])

    assert result.exit_code == 0
    assert "Preparing MICADO application' folders" in result.output

    # Check if the mocked functions were called with expected arguments
    mock_move_to_install_folder.assert_called_once_with("/fake/path")
    mock_download_release_tarball.assert_called_once_with("micado-eu", "micado_deployment", "v1_0_0")
    mock_extract_tarball.assert_called_once_with("/path/to/tarball")
    mock_delete_file.assert_called_once_with("/path/to/tarball")

if __name__ == "__main__":
    pytest.main()
