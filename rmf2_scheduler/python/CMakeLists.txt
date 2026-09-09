find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 REQUIRED)
find_package(pybind11_json REQUIRED)

pybind11_add_module(_core
  src/cache/action.cpp
  src/cache/event_action.cpp
  src/cache/process_action.cpp
  src/cache/series_action.cpp
  src/cache/schedule_cache.cpp
  src/cache/task_action.cpp
  src/core.cpp
  src/data/duration.cpp
  src/data/edge.cpp
  src/data/event.cpp
  src/data/graph.cpp
  src/data/node.cpp
  src/data/process.cpp
  src/data/task.cpp
  src/data/series.cpp
  src/data/occurrence.cpp
  src/data/time.cpp
  src/data/time_window.cpp
  src/data/schedule_action.cpp
  src/data/schedule_change_record.cpp
  src/executor_data.cpp
  src/process_executor.cpp
  src/process_executor_taskflow.cpp
  src/py_utils.cpp
  src/scheduler.cpp
  src/scheduler_options.cpp
  src/storage/schedule_stream.cpp
  src/system_time_executor.cpp
  src/task_executor.cpp
  src/task_executor_manager.cpp
)

target_link_libraries(_core
  PUBLIC
    rmf2_scheduler::rmf2_scheduler
  PRIVATE
    nlohmann_json::nlohmann_json
    pybind11_json
)

target_include_directories(_core
  PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

if(SKBUILD)
  # Install for scikit-build-core
  install(TARGETS
    _core
    DESTINATION .
  )

  # Manual RPATH patching
  if(APPLE)
    set(origin_token "@loader_path")
  else()
    set(origin_token "$ORIGIN")
  endif()
  set_target_properties(_core
    PROPERTIES
      INSTALL_RPATH "${origin_token}/lib"
  )
else()
  find_package(ament_cmake_python QUIET)

  if(NOT ament_cmake_python_FOUND)
    message(WARNING
      "Python build with CMake only detected, some functions are not supported. "
      "(For example, `pip show rmf2_scheduler`)\n"
      "Switch to using scikit-build-core or ament_cmake_python instead!"
    )

    set(PYTHON_INSTALL_DIR "local/lib/python${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}/site-packages")

    install(
      DIRECTORY ${PROJECT_NAME}/
      DESTINATION ${PYTHON_INSTALL_DIR}/${PROJECT_NAME}
    )
  else()
    ament_python_install_package(${PROJECT_NAME})
  endif()

  install(TARGETS
    _core
    DESTINATION ${PYTHON_INSTALL_DIR}/${PROJECT_NAME}
  )

  # export python path as hooks used by ament_cmake
  file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/share/${PROJECT_NAME}/hook/pythonpath.dsv
    "prepend-non-duplicate;PYTHONPATH;${PYTHON_INSTALL_DIR}")
  install(
    FILES ${CMAKE_CURRENT_BINARY_DIR}/share/${PROJECT_NAME}/hook/pythonpath.dsv
    DESTINATION share/${PROJECT_NAME}/hook
  )
endif()
