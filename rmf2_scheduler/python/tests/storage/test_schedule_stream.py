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

from rmf2_scheduler.cache import ScheduleCache
from rmf2_scheduler.data import TimeWindow
from rmf2_scheduler.storage import ScheduleStream


def test_read_schedule_success(mock_schedule_stream):
    mock_schedule_stream.mock.read_schedule.return_value = (True, "")

    result, error = ScheduleStream.read_schedule(
        mock_schedule_stream, ScheduleCache(), TimeWindow()
    )

    assert result
    assert error == ""
    assert mock_schedule_stream.mock.read_schedule.call_count == 1


def test_read_schedule_propagates_failure(mock_schedule_stream):
    mock_schedule_stream.mock.read_schedule.return_value = (False, "read failed")

    result, error = ScheduleStream.read_schedule(
        mock_schedule_stream, ScheduleCache(), TimeWindow()
    )

    assert not result
    assert error == "read failed"


def test_read_schedule_invalid_return_type(mock_schedule_stream):
    mock_schedule_stream.mock.read_schedule.return_value = "not a tuple"

    result, error = ScheduleStream.read_schedule(
        mock_schedule_stream, ScheduleCache(), TimeWindow()
    )

    assert not result
    assert "Invalid Python return type" in error


def test_read_schedule_invalid_number_of_returns(mock_schedule_stream):
    mock_schedule_stream.mock.read_schedule.return_value = (True,)

    result, error = ScheduleStream.read_schedule(
        mock_schedule_stream, ScheduleCache(), TimeWindow()
    )

    assert not result
    assert "Invalid number of returns" in error


def test_write_schedule_time_window_overload(mock_schedule_stream):
    mock_schedule_stream.mock.write_schedule.return_value = (True, "")

    result, error = ScheduleStream.write_schedule(
        mock_schedule_stream, ScheduleCache(), TimeWindow()
    )

    assert result
    assert error == ""


def test_write_schedule_records_overload(mock_schedule_stream):
    mock_schedule_stream.mock.write_schedule.return_value = (True, "")

    result, error = ScheduleStream.write_schedule(
        mock_schedule_stream, ScheduleCache(), []
    )

    assert result
    assert error == ""
    assert mock_schedule_stream.mock.write_schedule.call_count == 1


def test_write_schedule_propagates_failure(mock_schedule_stream):
    mock_schedule_stream.mock.write_schedule.return_value = (False, "write failed")

    result, error = ScheduleStream.write_schedule(
        mock_schedule_stream, ScheduleCache(), TimeWindow()
    )

    assert not result
    assert error == "write failed"


def test_refresh_tasks_success(mock_schedule_stream):
    mock_schedule_stream.mock.refresh_tasks.return_value = (True, "")

    result, error = ScheduleStream.refresh_tasks(
        mock_schedule_stream, ScheduleCache(), ["task_1", "task_2"]
    )

    assert result
    assert error == ""
    mock_schedule_stream.mock.refresh_tasks.assert_called_once()
    called_ids = mock_schedule_stream.mock.refresh_tasks.call_args[0][1]
    assert called_ids == ["task_1", "task_2"]


def test_refresh_tasks_propagates_failure(mock_schedule_stream):
    mock_schedule_stream.mock.refresh_tasks.return_value = (False, "refresh failed")

    result, error = ScheduleStream.refresh_tasks(
        mock_schedule_stream, ScheduleCache(), []
    )

    assert not result
    assert error == "refresh failed"


def test_missing_override_fails_gracefully():
    class BareScheduleStream(ScheduleStream):
        pass

    result, error = ScheduleStream.read_schedule(
        BareScheduleStream(), ScheduleCache(), TimeWindow()
    )

    assert not result
    assert "cannot find defined Python function" in error
