from enum import Enum
from io import TextIOWrapper
import itertools
import json
import os
from typing import List

def get_all_files(dir: str) -> List[str]:
    return [
        os.path.join(dir, file)
        for file in os.listdir(dir)
        if os.path.isfile(os.path.join(dir, file))
    ]

def get_filename(path: str) -> str:
    name, _ = os.path.splitext(os.path.basename(path))
    return name

def format_cell(cell: List[str]) -> List[str]:
    try:
        if not cell[-1].endswith("\n"):
            cell[-1] += "\n\n"
        elif not cell[-1].endswith("\n\n"):
            cell[-1] += "\n"
    except IndexError:
        cell.append("\n\n\n")
    return cell

class FileType(Enum):
    PY = 1
    IPYNB = 2

def format_file(filename: str, filetype: FileType) -> str:
    if filetype == FileType.PY:
        return filename if filename.endswith(".py") else filename + ".py"
    elif filetype == FileType.IPYNB:
        return filename if filename.endswith(".ipynb") else filename + ".ipynb"

def convert_ipynb(src: TextIOWrapper, dest: TextIOWrapper):
    dest.writelines(
        list(itertools.chain(*[
            format_cell(cell["source"])
            for cell in json.load(src)["cells"]
            if cell["cell_type"] == "code"
        ]))
    )

def convert(src: str, dest: str, dir="./"):
    with (
        open(os.path.join(dir, format_file(src, FileType.IPYNB)), "r") as src,
        open(os.path.join(dir, format_file(dest, FileType.PY)), "w+") as dest
    ):
        convert_ipynb(src, dest)

def convert_dir(dir: str, output_dir: str):
    [convert(src, os.path.join(output_dir, get_filename(src))) for src in get_all_files(dir)]

if __name__ == "__main__":
    filename = "01_notebook"
    convert(filename, f"outputs/{filename}", dir="./examples/convert/")

    lib_path = "./examples/convert/02_multiple"
    convert_dir(lib_path, f"{lib_path}/outputs/")