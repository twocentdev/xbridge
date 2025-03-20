import logging
import shutil
import subprocess
from pathlib import Path


logger = logging.getLogger(__name__)


def unpack_7z(file_path: Path, target_path: Path):
    # Check inputs, for security reasons.
    if not __is_valid_7z(file_path):
        err_msg = "File to unpack not found."
        logger.fatal(err_msg)
        raise FileNotFoundError(err_msg)
    if not (target_path.exists() and target_path.is_dir()):
        err_msg = "Temp file not found or is not a dir."
        logger.fatal(err_msg)
        raise FileNotFoundError(err_msg)
    cmd = [shutil.which('7z'), 'x', f'-o{target_path}', file_path, '*.json',
           '*dim-def.xml', '-r']
    if not cmd[0]:
        err_msg = "7z executable not found"
        logger.fatal(err_msg)
        raise FileNotFoundError(err_msg)
    process = subprocess.run(cmd, capture_output=True)
    if process.returncode != 0:
        err_msg = "Error extracting file"
        logger.fatal(err_msg)
        raise ValueError(err_msg)

def __is_valid_7z(file_path: Path) -> bool:
    return (
        file_path.exists()
        and file_path.is_file()
        and file_path.suffix == ".7z"
    )

def __is_valid_path(file_path: Path) -> bool:
    return (
            file_path.exists()
            and not str(file_path).startswith("__MACOSX")
            and not ".DS_Store" in str(file_path)
            and "/tab/" in str(file_path)
    )
