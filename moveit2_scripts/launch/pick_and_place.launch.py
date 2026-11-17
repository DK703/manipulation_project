import os
from launch import LaunchDescription
from launch.actions import TimerAction
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("name", package_name="my_moveit_config").to_moveit_configs()

    #perception server

    perception_node = Node(
        package="simple_grasping",
        executable="basic_grasping_perception_node",
        name="basic_grasping_perception",
        output="screen",
        parameters=[
            {"debug_topics": True},
            {"use_sim_time": True},
        ],
    )


    # MoveItCpp demo executable
    moveit_cpp_node = Node(
        name="pick_and_place",
        package="moveit2_scripts",
        executable="pick_and_place",
        output="screen",
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            {'use_sim_time': True},
        ],
    )
    delayed_pick_and_place = TimerAction(period=5.0, actions=[moveit_cpp_node])
    return LaunchDescription(
        [perception_node, delayed_pick_and_place]
    )