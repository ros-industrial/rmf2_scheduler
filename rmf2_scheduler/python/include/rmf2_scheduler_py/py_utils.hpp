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

#ifndef RMF2_SCHEDULER_PY__PY_UTILS_HPP_
#define RMF2_SCHEDULER_PY__PY_UTILS_HPP_

#include <pybind11/pybind11.h>

#include <string>

namespace py = pybind11;

namespace py_utils
{

void def_str_const(
  py::module & m,
  const char * name,
  const char * value
);

}  // namespace py_utils

/**
 * Similar to PYBIND11_OVERRIDE_PURE, but the python function returns (bool, str, ...)
 * as a tuple tuple to better follow python conventions
 *
 *   bool fn(Args... args, std::string & error) override
 *   {
 *     RS_PYBIND11_OVERRIDE_PURE_WITH_BOOL_ERROR(ClassName, fn, args...);
 *   }
 *
 * This macro is wrapped in do-while(false), mirroring PYBIND11_OVERRIDE_IMPL, so the
 * macro expands to a single statement (safe inside a bare `if`/`else`).
 */
#define RS_PYBIND11_OVERRIDE_PURE_WITH_BOOL_ERROR(class_name, fn, ...) \
  do { \
    /* Acquire the GIL while while in this scope */ \
    py::gil_scoped_acquire gil; \
 \
    /* Look up the same-named Python override on the instance. */ \
    py::function override = py::get_override(this, #fn); \
    if (!override) { \
      error = #class_name " " #fn " failed: cannot find defined Python function"; \
      return false; \
    } \
 \
    /* Call it and validate it honored the (bool, str) return contract. */ \
    auto obj = override (__VA_ARGS__); \
    if (!py::isinstance<py::tuple>(obj)) { \
      error = #class_name " " #fn " failed: Invalid Python return type."; \
      return false; \
    } \
    py::tuple tuple_obj = obj; \
    if (py::len(tuple_obj) != 2) { \
      error = #class_name " " #fn " failed: Invalid number of returns"; \
      return false; \
    } \
 \
    /* Unpack it: propagate the error on failure, otherwise succeed. */ \
    bool result = tuple_obj[0].cast<bool>(); \
    if (!result) { \
      error = tuple_obj[1].cast<std::string>(); \
      return false; \
    } \
    return true; \
  } while (false)

#endif  // RMF2_SCHEDULER_PY__PY_UTILS_HPP_
