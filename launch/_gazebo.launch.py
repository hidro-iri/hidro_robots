import sys
import os
import xacro

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription, LaunchService
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution, Command, LaunchConfiguration, TextSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    ld = LaunchDescription()

    # Remember to add plugin paths to "GAZEBO_PLUGIN_PATH"

    robot_name_arg = DeclareLaunchArgument('robot_name', description="robot", default_value='')

    ld.add_action(robot_name_arg)

    # GAZEBO
    world_filename = PathJoinSubstitution([FindPackageShare("hidro_robots"), "worlds", "basic_world.world"])

    gazebo = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        [PathJoinSubstitution([FindPackageShare("gazebo_ros"), "launch", "gazebo.launch.py"])]),
                                      launch_arguments={
                                          "verbose": "false",
                                          "pause": "false",
                                          "world": world_filename,
                                      }.items())

    ld.add_action(gazebo)

    # XACRO GAZEBO
    robot_description_content = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]), " ",
        PathJoinSubstitution([
            FindPackageShare("hidro_robots"),
            "robots",
            LaunchConfiguration("robot_name"),
            "xacro",
            "description.urdf.xacro",
        ])
    ])

    robot_description = {"robot_description": robot_description_content}

    # ROBOT STATE PUBLISHER GAZEBO
    node_robot_state_publisher = Node(package="robot_state_publisher",
                                      executable="robot_state_publisher",
                                      output="screen",
                                      namespace="gazebo",
                                      parameters=[robot_description])

    ld.add_action(node_robot_state_publisher)

    # SPAWN ENTITY
    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic", ["gazebo", "/robot_description"], "-entity",
            LaunchConfiguration('robot_name'), "-x 0", "-y 0", "-z 0.3"
        ],
        output="screen",
    )
    ld.add_action(spawn_entity)

    return ld


if __name__ == '__main__':
    ls = LaunchService()
    ls.include_launch_description(generate_launch_description())
    sys.exit(ls.run())