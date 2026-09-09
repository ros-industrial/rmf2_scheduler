#!/bin/bash
# Install native build deps for rmf2_scheduler
# (nlohmann_json, pybind11, pybind11_json, croncpp, Taskflow, curl, Boost).
set -euo pipefail

NLOHMANN_JSON_TAG="${NLOHMANN_JSON_TAG:-9cca280a4d0ccf0c08f47a99aa71d1b0e52f8d03}"  # v3.11.3
PYBIND11_TAG="${PYBIND11_TAG:-a2e59f0e7065404b44dfe92a28aca47ba1378dc4}"            # v2.13.6
PYBIND11_JSON_TAG="${PYBIND11_JSON_TAG:-b02a2ad597d224c3faee1f05a56d81d4c4453092}"  # 0.2.13
INSTALL_PREFIX="${CMAKE_INSTALL_PREFIX:-/usr/local}"

git_shallow_clone() {
  if [ $# -lt 3 ]; then
    echo "Usage: git_shallow_clone <repo_url> <repo_dir> <repo_tag>"
    exit 1
  fi
  local repo_url=$1; shift
  local repo_dir=$1; shift
  local repo_tag=$1; shift

  mkdir "$repo_dir"
  git -C "$repo_dir" init -q
  git -C "$repo_dir" remote add origin "$repo_url"
  git -C "$repo_dir" fetch --depth 1 origin "$repo_tag"
  git -C "$repo_dir" checkout -q FETCH_HEAD
}

install_json_from_source() {
  local work
  work="$(mktemp -d)"

  git_shallow_clone \
    https://github.com/nlohmann/json.git "$work/json" "$NLOHMANN_JSON_TAG"
  cmake -S "$work/json" -B "$work/json/build" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="$INSTALL_PREFIX" \
    -DJSON_BuildTests=OFF
  cmake --install "$work/json/build"

  rm -rf "$work"
}

# Header-only pybind11 CMake package. PYBIND11_NOPYTHON avoids baking the
# container interpreter; the wheel build gets pybind11 from build-system.requires.
install_pybind11_from_source() {
  local work
  work="$(mktemp -d)"

  git_shallow_clone \
    https://github.com/pybind/pybind11.git "$work/pybind11" "$PYBIND11_TAG"
  cmake -S "$work/pybind11" -B "$work/pybind11/build" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="$INSTALL_PREFIX" \
    -DPYBIND11_TEST=OFF \
    -DPYBIND11_NOPYTHON=ON
  cmake --build "$work/pybind11/build" --parallel
  cmake --install "$work/pybind11/build"

  rm -rf "$work"
}

# pybind11_json: header-only bridge between nlohmann::json and pybind11.
install_pybind11_json_from_source() {
  local work
  work="$(mktemp -d)"

  git_shallow_clone \
    https://github.com/pybind/pybind11_json.git "$work/pb11j" "$PYBIND11_JSON_TAG"
  cmake -S "$work/pb11j" -B "$work/pb11j/build" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="$INSTALL_PREFIX" \
    -DCMAKE_PREFIX_PATH="${INSTALL_PREFIX}${CMAKE_PREFIX_PATH:+:${CMAKE_PREFIX_PATH}}" \
    -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
    -DPYTHON_INCLUDE_DIRS=
  cmake --build "$work/pb11j/build" --parallel
  cmake --install "$work/pb11j/build"

  rm -rf "$work"
}

install_linux() {
  if command -v yum >/dev/null 2>&1; then
    yum install -y cmake git libcurl-devel boost-devel
  elif command -v apk >/dev/null 2>&1; then
    apk add --no-cache cmake git curl-dev boost-dev
  else
    echo "Unsupported Linux package manager" >&2
    exit 1
  fi

  install_json_from_source
  install_pybind11_from_source
  install_pybind11_json_from_source
}

install_macos() {
  brew install cmake git curl boost

  INSTALL_PREFIX="${CMAKE_INSTALL_PREFIX:-$(brew --prefix)}"
  export CMAKE_PREFIX_PATH="$INSTALL_PREFIX"

  install_json_from_source
  install_pybind11_from_source
  install_pybind11_json_from_source
}

case "$(uname -s)" in
  Linux)
    install_linux
    ;;
  Darwin)
    install_macos
    ;;
  *)
    echo "Unsupported OS: $(uname -s)" >&2
    exit 1
    ;;
esac

echo "All native dependencies installed!"
