import sys
import os
import xacro

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription, LaunchService
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution, Command, LaunchConfiguration, TextSubstitution, PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    ld = LaunchDescription()

    # Remember to add plugin paths to "GAZEBO_PLUGIN_PATH"

    robot_name_arg = DeclareLaunchArgument('robot_name', description="robot", default_value='')

    ld.add_action(robot_name_arg)

    event_based_sim_arg = DeclareLaunchArgument('event_based_sim',
                                                description='Run event based simulation',
                                                default_value='False')
    ld.add_action(event_based_sim_arg)

    # GAZEBO
    world_filename = PythonExpression(
        ["'event_based.world' if ",
         LaunchConfiguration('event_based_sim'), " else 'basic_world.world'"])
    world_path = PathJoinSubstitution([FindPackageShare("hidro_robots"), "worlds", world_filename])

    enable_gui = PythonExpression(["'false' if ", LaunchConfiguration('event_based_sim'), " else 'true'"])

    gazebo = IncludeLaunchDescription(PythonLaunchDescriptionSource(
        [PathJoinSubstitution([FindPackageShare("gazebo_ros"), "launch", "gazebo.launch.py"])]),
                                      launch_arguments={
                                          "verbose": "true",
                                          "pause": "false",
                                          "world": world_path,
                                          "lockstep": "true",
                                          "gui": enable_gui,
                                      }.items())

    ld.add_action(gazebo)

    # XACRO GAZEBO
    robot_description_content = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]), " ",
        PathJoinSubstitution([
            FindPackageShare("hidro_robots"), "robots",
            LaunchConfiguration("robot_name"), "xacro", "description.urdf.xacro"
        ]), " event_based_sim:=",
        LaunchConfiguration("event_based_sim")
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