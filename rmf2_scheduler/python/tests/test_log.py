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
import subprocess
import sys

import pytest
from rmf2_scheduler import log
from rmf2_scheduler.log import register_python_logger


@pytest.fixture(autouse=True)
def _restore_log_state():
    original_level = log.get_log_level()
    yield
    log.unregister_log_handler()
    log.set_log_level(original_level)


def test_register_log_handler_receives_message():
    received = []
    log.register_log_handler(
        lambda file, line, loglevel, message: received.append(
            (file, line, loglevel, message)
        )
    )
    log.set_log_level(log.LogLevel.DEBUG)

    log.log("test_file.cpp", 42, log.LogLevel.WARN, "hello world")

    assert received == [("test_file.cpp", 42, log.LogLevel.WARN, "hello world")]


def test_log_below_current_level_is_dropped():
    received = []
    log.register_log_handler(lambda *args: received.append(args))
    log.set_log_level(log.LogLevel.ERROR)

    log.log("test_file.cpp", 1, log.LogLevel.INFO, "should not show up")

    assert received == []


def test_unregister_log_handler_restores_default():
    received = []
    log.register_log_handler(lambda *args: received.append(args))
    log.set_log_level(log.LogLevel.DEBUG)
    log.unregister_log_handler()

    log.log("test_file.cpp", 1, log.LogLevel.INFO, "default handler now")

    assert received == []


def test_set_and_get_log_level_round_trip():
    log.set_log_level(log.LogLevel.ERROR)

    assert log.get_log_level() == log.LogLevel.ERROR


@pytest.mark.parametrize(
    "native_level,expected_level",
    [
        (log.LogLevel.DEBUG, logging.DEBUG),
        (log.LogLevel.INFO, logging.INFO),
        (log.LogLevel.WARN, logging.WARNING),
        (log.LogLevel.ERROR, logging.ERROR),
        (log.LogLevel.FATAL, logging.CRITICAL),
    ],
)
def test_register_python_logger_maps_levels(caplog, native_level, expected_level):
    register_python_logger()
    log.set_log_level(log.LogLevel.DEBUG)

    with caplog.at_level(logging.DEBUG, logger="rmf2_scheduler.log"):
        log.log("test_file.cpp", 1, native_level, "native message")

    assert len(caplog.records) == 1
    assert caplog.records[0].levelno == expected_level
    assert caplog.records[0].message == "native message"


def test_register_python_logger_drops_none_level(caplog):
    # NONE maps to logging.NOTSET, which Python's logging module never
    # actually emits records for (isEnabledFor(NOTSET) is always False).
    register_python_logger()
    log.set_log_level(log.LogLevel.DEBUG)

    with caplog.at_level(logging.DEBUG, logger="rmf2_scheduler.log"):
        log.log("test_file.cpp", 1, log.LogLevel.NONE, "never emitted")

    assert caplog.records == []


def test_python_log_handler_survives_interpreter_shutdown():
    # Importing rmf2_scheduler registers a Python callback (register_python_logger)
    # as the native log handler. Without unregistering it before interpreter
    # shutdown, dropping that callback crashes the process (GIL/thread state
    # already gone by then) -- this must run in a subprocess to observe that.
    result = subprocess.run(
        [sys.executable, "-c", "import rmf2_scheduler"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Fatal Python error" not in result.stderr
