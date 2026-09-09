cmake_minimum_required(VERSION 3.8)

project(rmf2_scheduler VERSION 0.1.0)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(Boost REQUIRED)
find_package(nlohmann_json REQUIRED)
include(GNUInstallDirs)
include(cmake/fetch_deps.cmake)

add_library(${PROJECT_NAME}
  SHARED
  src/cache/action.cpp
  src/cache/event_action.cpp
  src/cache/task_action.cpp
  src/cache/task_handler.cpp
  src/cache/process_action.cpp
  src/cache/process_handler.cpp
  src/cache/series_action.cpp
  src/cache/series_handler.cpp
  src/cache/schedule_cache.cpp
  src/data/duration.cpp
  src/data/time.cpp
  src/data/node.cpp
  src/data/graph.cpp
  src/data/schedule_action.cpp
  src/data/schedule_change_record.cpp
  src/data/series.cpp
  src/default_log_handler.cpp
  src/executor_data.cpp
  src/http/curl_api.cpp
  src/http/common.cpp
  src/http/connection_curl.cpp
  src/http/connection_fake.cpp
  src/http/memory_stream.cpp
  src/http/request.cpp
  src/http/transport.cpp
  src/http/transport_curl.cpp
  src/http/transport_fake.cpp
  src/log.cpp
  src/process_executor_taskflow.cpp
  src/scheduler.cpp
  src/scheduler_options.cpp
  src/storage/schedule_stream.cpp
  src/storage/schedule_stream_ld_broker.cpp
  src/storage/schedule_stream_simple.cpp
  src/system_time_executor.cpp
  src/task_executor_manager.cpp
  src/time_window_lookup.cpp
  src/utils/dag_helper.cpp
  src/utils/data_encoding.cpp
  src/utils/string_utils.cpp
  src/utils/url_utils.cpp
)

add_library(${PROJECT_NAME}::${PROJECT_NAME} ALIAS ${PROJECT_NAME})

target_include_directories(${PROJECT_NAME}
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

target_link_libraries(${PROJECT_NAME}
  PUBLIC
    Taskflow::Taskflow
    nlohmann_json::nlohmann_json
  PRIVATE
    croncpp::croncpp
    curl
)

target_compile_definitions(${PROJECT_NAME}
  PUBLIC
    BOOST_DLL_USE_STD_FS
)

option(BUILD_EXAMPLES "Build example executables" ON)
option(BUILD_PYTHON "Build Python bindings" ON)

if(BUILD_EXAMPLES)
  add_subdirectory(examples)
endif()

if(BUILD_PYTHON)
  add_subdirectory(python)
endif()

if(BUILD_TESTING)
  find_package(ament_cmake QUIET)
  if(ament_cmake_FOUND)
    find_package(ament_lint_auto REQUIRED)
    ament_lint_auto_find_test_dependencies()
  endif()

  add_subdirectory(test)
endif()

install(TARGETS
  ${PROJECT_NAME}
  EXPORT export_${PROJECT_NAME}
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
  RUNTIME DESTINATION bin
)


install(
  DIRECTORY include/
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(EXPORT export_${PROJECT_NAME}
  NAMESPACE ${PROJECT_NAME}::
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}
  FILE ${PROJECT_NAME}Targets.cmake
)

include(CMakePackageConfigHelpers)
configure_package_config_file(
  cmake/${PROJECT_NAME}Config.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake
  INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}
)
write_basic_package_version_file(
  ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake
  VERSION ${PROJECT_VERSION}
  COMPATIBILITY SameMinorVersion
)

install(FILES
  ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake
  ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}
)

# Ament index and prefix-path hook for colcon/ROS 2 compatibility
file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/share/ament_index/resource_index/packages/${PROJECT_NAME} "")
install(
  FILES ${CMAKE_CURRENT_BINARY_DIR}/share/ament_index/resource_index/packages/${PROJECT_NAME}
  DESTINATION share/ament_index/resource_index/packages
)

file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/share/${PROJECT_NAME}/hook/ament_prefix_path.dsv
  "prepend-non-duplicate;AMENT_PREFIX_PATH;")
install(
  FILES ${CMAKE_CURRENT_BINARY_DIR}/share/${PROJECT_NAME}/hook/ament_prefix_path.dsv
  DESTINATION share/${PROJECT_NAME}/hook
)
