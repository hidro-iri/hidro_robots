from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution, Command, LaunchConfiguration
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
                                          "pause": "true",
                                          "world": world_filename,
                                      }.items())

    ld.add_action(gazebo)

    # XACRO
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

    # ROBOT STATE PUBLISHER
    node_robot_state_publisher = Node(package="robot_state_publisher",
                                      executable="robot_state_publisher",
                                      output="screen",
                                      parameters=[robot_description])

    ld.add_action(node_robot_state_publisher)

    # SPAWN ENTITY
    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic", "robot_description", "-entity",
            LaunchConfiguration('robot_name'), "-x 0", "-y 0", "-z 0.3"
        ],
        output="screen",
    )
    ld.add_action(spawn_entity)

    return ld
