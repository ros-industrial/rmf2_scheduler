// Copyright 2025 ROS Industrial Consortium Asia Pacific
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <pybind11/stl.h>

#include "rmf2_scheduler_py/process_executor.hpp"
#include "rmf2_scheduler_py/py_utils.hpp"
#include "rmf2_scheduler/process_executor.hpp"

namespace rmf2_scheduler
{

class PyProcessExecutor : public ProcessExecutor
{
public:
  using ProcessExecutor::ProcessExecutor;

  /// Trampoline
  bool run_async(
    const data::Process::ConstPtr & process,
    const std::vector<data::Task::ConstPtr> & tasks,
    std::string & error
  ) override
  {
    RS_PYBIND11_OVERRIDE_PURE_WITH_BOOL_ERROR(ProcessExecutor, run_async, process, tasks);
  }
};

}  // namespace rmf2_scheduler

namespace rmf2_scheduler_py
{
void init_process_executor_py(py::module & m)
{
  using namespace rmf2_scheduler;  // NOLINT(build/namespaces)

  py::class_<ProcessExecutor, PyProcessExecutor, ProcessExecutor::Ptr>(
    m,
    "ProcessExecutor"
  )
  .def(py::init<>())
  .def(
    "run_async",
    [](
      ProcessExecutor & self,
      const data::Process::ConstPtr & process,
      const std::vector<data::Task::ConstPtr> & tasks
    ) {
      std::string error;
      bool result = self.run_async(process, tasks, error);
      return std::make_tuple(result, error);
    }
  )
  ;
}

}  // namespace rmf2_scheduler_py
