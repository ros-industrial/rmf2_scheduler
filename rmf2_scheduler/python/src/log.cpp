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

#include <pybind11/functional.h>

#include <functional>
#include <memory>
#include <string>
#include <utility>

#include "rmf2_scheduler_py/log.hpp"
#include "rmf2_scheduler/log.hpp"

namespace rmf2_scheduler
{

namespace log
{

/// Adapts a std::function into a LogHandler, so callers can register a
/// callback instead of subclassing a pybind11-exposed base class (which
/// would otherwise need a std::unique_ptr<LogHandler> argument caster that
/// pybind11 doesn't provide). Plain C++ (no pybind dependency); the Python
/// binding only supplies the callback itself.
class FunctionLogHandler : public LogHandler
{
public:
  using Callback = std::function<void (const char *, int, LogLevel, const char *)>;

  explicit FunctionLogHandler(Callback callback)
  : callback_(std::move(callback))
  {
  }

  void log(const char * file, int line, LogLevel loglevel, const char * log) override
  {
    callback_(file, line, loglevel, log);
  }

private:
  Callback callback_;
};

}  // namespace log

}  // namespace rmf2_scheduler

namespace rmf2_scheduler_py
{

void init_log_py(py::module & m)
{
  using namespace rmf2_scheduler;  // NOLINT(build/namespaces)
  using namespace rmf2_scheduler::log;  // NOLINT(build/namespaces)

  py::module m_log = m.def_submodule("log");

  py::enum_<LogLevel>(m_log, "LogLevel")
    .value("DEBUG", LogLevel::DEBUG)
    .value("INFO", LogLevel::INFO)
    .value("WARN", LogLevel::WARN)
    .value("ERROR", LogLevel::ERROR)
    .value("FATAL", LogLevel::FATAL)
    .value("NONE", LogLevel::NONE)
  ;

  m_log.def(
    "log",
    [](const std::string & file, int line, LogLevel loglevel, const std::string & message) {
      rmf2_scheduler::log::log(file.c_str(), line, loglevel, "%s", message.c_str());
    },
    py::arg("file"),
    py::arg("line"),
    py::arg("loglevel"),
    py::arg("message"),
    "Emit a log message through the currently registered log handler."
  );
  m_log.def(
    "register_log_handler",
    [](FunctionLogHandler::Callback callback) {
      registerLogHandler(
        std::make_unique<FunctionLogHandler>(
          [callback](const char * file, int line, LogLevel loglevel, const char * log) {
            py::gil_scoped_acquire gil;
            callback(file, line, loglevel, log);
          }
        )
      );
    },
    py::arg("callback"),
    "Register callback(file, line, loglevel, log) to handle log messages."
  );
  m_log.def(
    "unregister_log_handler",
    &unregisterLogHandler,
    "Unregister current log handler, this will enable default log handler."
  );
  m_log.def(
    "set_log_level",
    &setLogLevel,
    "Set log level this will disable messages with lower log level."
  );
  m_log.def(
    "get_log_level",
    &getLogLevel,
    "Get current log level."
  );

  py::module_::import("atexit").attr("register")(py::cpp_function(&unregisterLogHandler));
}

}  // namespace rmf2_scheduler_py
