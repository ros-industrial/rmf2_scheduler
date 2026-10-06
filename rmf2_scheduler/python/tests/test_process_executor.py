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

from rmf2_scheduler import ProcessExecutor
from rmf2_scheduler.data import Process, Task


def test_run_async_success(mock_process_executor):
    mock_process_executor.mock.run_async.return_value = (True, "")

    result, error = ProcessExecutor.run_async(
        mock_process_executor, Process(), [Task()]
    )

    assert result
    assert error == ""
    mock_process_executor.mock.run_async.assert_called_once()


def test_run_async_propagates_failure(mock_process_executor):
    mock_process_executor.mock.run_async.return_value = (False, "run failed")

    result, error = ProcessExecutor.run_async(mock_process_executor, Process(), [])

    assert not result
    assert error == "run failed"


def test_run_async_invalid_return_type(mock_process_executor):
    mock_process_executor.mock.run_async.return_value = "not a tuple"

    result, error = ProcessExecutor.run_async(mock_process_executor, Process(), [])

    assert not result
    assert "Invalid Python return type" in error


def test_run_async_invalid_number_of_returns(mock_process_executor):
    mock_process_executor.mock.run_async.return_value = (True,)

    result, error = ProcessExecutor.run_async(mock_process_executor, Process(), [])

    assert not result
    assert "Invalid number of returns" in error


def test_run_async_missing_override():
    class BareProcessExecutor(ProcessExecutor):
        pass

    result, error = ProcessExecutor.run_async(BareProcessExecutor(), Process(), [])

    assert not result
    assert "cannot find defined Python function" in error
