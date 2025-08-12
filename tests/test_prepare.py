# tests/test_prepare.py
from enum import Enum
from typer.testing import CliRunner
from unittest.mock import patch
import importlib

runner = CliRunner()

@patch("app.core.git.download_release_tarball")
@patch("app.core.git.get_github_releases_enum")
@patch("app.core.fileops.move_to_install_folder")
@patch("app.core.fileops.extract_tarball")
@patch("app.core.fileops.delete_file")
def test_download(mock_delete, mock_extract, mock_move, mock_get_releases, mock_dl, tmp_path):
    # Make the mocked function return a single allowed release
    mock_get_releases.return_value = [("v1_0_0", "v1_0_0")]
    mock_dl.return_value = "/path/to/tarball"

    # Import (or reload) AFTER patches so the Enum is built from the mocked list
    prepare_mod = importlib.import_module("app.commands.prepare")
    prepare_mod = importlib.reload(prepare_mod)

    result = runner.invoke(prepare_mod.app, [
        "--release", "v1_0_0",
        "--path", str(tmp_path),   # always exists
    ])

    assert result.exit_code == 0, result.output
    mock_move.assert_called_once_with(str(tmp_path))
    mock_extract.assert_called_once_with("/path/to/tarball")
    mock_delete.assert_called_once_with("/path/to/tarball")
