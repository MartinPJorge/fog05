#!/usr/bin/env bash

source /opt/ros/r2b3/setup.bash

source /opt/ros/r2b3/share/ros2cli/environment/ros2-argcomplete.bash

ament build_pkg {{ node_path }} --build-space {{ space }} --install-space {{ space }}


