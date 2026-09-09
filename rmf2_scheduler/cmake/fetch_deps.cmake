# If croncpp or Taskflow are not found on the system, download them via CPM.
# Set RMF2_SCHEDULER_FETCH_DEPS=OFF to disable auto-fetching and require system packages.
option(RMF2_SCHEDULER_FETCH_DEPS
  "Fetch missing dependencies with CPM if not found on system" ON)

find_package(croncpp QUIET)
find_package(Taskflow QUIET)

if(RMF2_SCHEDULER_FETCH_DEPS AND (NOT croncpp_FOUND OR NOT Taskflow_FOUND))
  set(CPM_DOWNLOAD_VERSION 0.40.2)
  set(_cpm_file "${CMAKE_CURRENT_BINARY_DIR}/CPM_${CPM_DOWNLOAD_VERSION}.cmake")
  if(NOT EXISTS "${_cpm_file}")
    file(DOWNLOAD
      "https://github.com/cpm-cmake/CPM.cmake/releases/download/v${CPM_DOWNLOAD_VERSION}/CPM.cmake"
      "${_cpm_file}"
    )
  endif()
  include("${_cpm_file}")
  unset(_cpm_file)
endif()

if(NOT croncpp_FOUND)
  if(NOT RMF2_SCHEDULER_FETCH_DEPS)
    find_package(croncpp REQUIRED)
  else()
    message(STATUS "croncpp not found, fetching with CPM...")
    CPMAddPackage(
      NAME croncpp
      GIT_REPOSITORY https://github.com/mariusbancila/croncpp
      GIT_TAG e817348a2dcd77b968c0b87a43274932b9800f4b  # v2023.03.30
      OPTIONS "CRONCPP_BUILD_TESTS OFF" "CRONCPP_BUILD_BENCHMARK OFF"
      PATCHES "${CMAKE_CURRENT_LIST_DIR}/patches/croncpp_include_dir.patch"
      GIT_SHALLOW TRUE
      EXCLUDE_FROM_ALL YES
    )
  endif()
endif()

if(NOT Taskflow_FOUND)
  if(NOT RMF2_SCHEDULER_FETCH_DEPS)
    find_package(Taskflow REQUIRED)
  else()
    message(STATUS "Taskflow not found, fetching with CPM...")
    CPMAddPackage(
      NAME Taskflow
      GIT_REPOSITORY https://github.com/taskflow/taskflow
      GIT_TAG 816b4ad53b44196c88f409eb7b4a25a0e3bfdf42  # v3.11.0
      OPTIONS "TF_BUILD_TESTS OFF" "TF_BUILD_EXAMPLES OFF"
      GIT_SHALLOW TRUE
      EXCLUDE_FROM_ALL YES
    )
  endif()
endif()
