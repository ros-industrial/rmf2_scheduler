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

import logging

from ._core.log import *
from ._core.log import LogLevel, register_log_handler

_LOGGER = logging.getLogger(__name__)

_LEVEL_TO_LOGGING = {
    LogLevel.DEBUG: logging.DEBUG,
    LogLevel.INFO: logging.INFO,
    LogLevel.WARN: logging.WARNING,
    LogLevel.ERROR: logging.ERROR,
    LogLevel.FATAL: logging.CRITICAL,
    LogLevel.NONE: logging.NOTSET,
}


def _log_callback(file: str, line: int, loglevel: LogLevel, log: str) -> None:
    _LOGGER.log(_LEVEL_TO_LOGGING[loglevel], log)


def register_python_logger() -> None:
    """Register a callback that forwards every native log message to a Python logger."""
    register_log_handler(_log_callback)
