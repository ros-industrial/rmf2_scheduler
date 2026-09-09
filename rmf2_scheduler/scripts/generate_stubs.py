# Copyright 2025 ROS Industrial Consortium Asia Pacific
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from pathlib import Path

from pybind11_stubgen import main as stubgen_main

DIR = Path(__file__).parent.resolve()
HEADER_FILE = DIR / "stub_header.txt"


def _get_header(header_file):
    header = ""
    with open(header_file, "r") as f:
        for line in f:
            # strip trailing white space
            header += ("# " + line.rstrip("\n").rstrip("\r")).rstrip()
            header += "\n"

    return header


def _add_header(header, file):
    with open(file, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(header + "\n" + content)


def _get_output_dir():
    for i in range(len(sys.argv)):
        # reverse the search for the last defined option
        index = len(sys.argv) - i - 1
        value = sys.argv[index]

        if value == "-o" or value == "--output-dir":
            break

    # Set to default value
    if index == 0:
        return "./stub"

    return sys.argv[index + 1]


def _is_dry_run():
    return "--dry-run" in sys.argv


def post_main():
    if _is_dry_run():
        return

    print("post-processing: adding headers...")

    output_dir = _get_output_dir()
    header = _get_header(HEADER_FILE)
    print(f"headers found in {HEADER_FILE}")

    # Find all .log files recursively
    print(f"processing stub files (.pyi) in {output_dir}")
    for file_path in Path(output_dir).glob("**/*.pyi"):
        _add_header(header, file_path)

    print("post-processing: done")


def main():
    stubgen_main()
    post_main()


if __name__ == "__main__":
    main()
