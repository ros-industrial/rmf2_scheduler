# Build From Source

## Prerequisite

- Compiler: GCC 11+, Clang 14+
- OS: Ubuntu 22.04+
- Supported ROS2 distros
  - Humble
  - Jazzy

## Install ROS2

Follow the [official
documentation](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)
to install the latest binary release of ROS2.

Install all necessary additional dependencies:

```bash
sudo apt install -y python3-colcon-common-extensions \
                    python3-vcstool \
                    python3-rosdep
```

Remember to [initialize and update
rosdep](https://docs.ros.org/en/humble/Tutorials/Intermediate/Rosdep.html#how-do-i-use-the-rosdep-tool)
if it is your first time installing `rosdep`.

```bash
sudo rosdep init
rosdep update
```

**Append ROS2 environment in** `.bashrc` **(Optional)**

To ensure that the ROS2 environment is sourced automatically when the
terminal is started, append the following line to the end of the bash
configuration (in `~/.bashrc`):

```bash
source /opt/ros/humble/setup.bash
```

## Build & Install

Create a colcon workspace.

```bash
export COLCON_WS=~/colcon_ws
mkdir -p $COLCON_WS/src
cd $COLCON_WS
```

Download the source code

```bash
cd src
git clone https://github.com/ros-industrial/rmf_scheduler.git
```

Install dependencies.

```bash
rosdep install --from-paths . --ignore-src --rosdistro $ROS_DISTRO -y
```

Build.

```bash
cd ..
colcon build
```
