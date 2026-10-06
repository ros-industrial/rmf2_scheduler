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

from rmf2_scheduler import ExecutorData, TaskExecutor


def test_start_success(mock_task_executor):
    mock_task_executor.mock.start.return_value = (True, "")

    result, error = TaskExecutor.start(mock_task_executor, "task_id", ExecutorData())

    assert result
    assert error == ""
    mock_task_executor.mock.start.assert_called_once()


def test_start_propagates_failure(mock_task_executor):
    mock_task_executor.mock.start.return_value = (False, "start failed")

    result, error = TaskExecutor.start(mock_task_executor, "task_id", ExecutorData())

    assert not result
    assert error == "start failed"


def test_start_invalid_return_type(mock_task_executor):
    mock_task_executor.mock.start.return_value = "not a tuple"

    result, error = TaskExecutor.start(mock_task_executor, "task_id", ExecutorData())

    assert not result
    assert "Invalid Python return type" in error


def test_start_invalid_number_of_returns(mock_task_executor):
    mock_task_executor.mock.start.return_value = (True,)

    result, error = TaskExecutor.start(mock_task_executor, "task_id", ExecutorData())

    assert not result
    assert "Invalid number of returns" in error


def test_start_missing_override():
    class BareTaskExecutor(TaskExecutor):
        pass

    result, error = TaskExecutor.start(BareTaskExecutor(), "task_id", ExecutorData())

    assert not result
    assert "cannot find defined Python function" in error
