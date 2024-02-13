# BSD 3-Clause License

# Copyright (C) 2018-2020 LAAS-CNRS, University of Edinburgh, INRIA
# Copyright note valid unless otherwise stated in individual files.
# All rights reserved.

from os import path

import pinocchio
from hidro_robots.path import HIDRO_ROBOTS


class RobotLoader:

    def __init__(self, robot_name, urdf_filename):
        self.__urdf_filename = urdf_filename
        self.__robot_name = robot_name

        self.__urdf_path = path.join(
            HIDRO_ROBOTS, "robots", self.__robot_name, self.__urdf_filename
        )
        self.robot = pinocchio.RobotWrapper.BuildFromURDF(
            self.__urdf_path,
            HIDRO_ROBOTS + "/../",
            pinocchio.JointModelFreeFlyer(),
        )


class BorinotLoader(RobotLoader):
    def __init__(self):
        super().__init__("borinot", "borinot.urdf")


class BorinotFlyingArm2Loader(RobotLoader):
    def __init__(self):
        super().__init__("borinot_flying_arm_2", "borinot_flying_arm_2.urdf")


class Hexacopter370FlyingArm3Loader(RobotLoader):
    def __init__(self):
        super().__init__(
            "hexacopter370_flying_arm_3", "hexacopter370_flying_arm_3.urdf"
        )


class Hexacopter680FlyingArm2Loader(RobotLoader):
    def __init__(self):
        super().__init__(
            "hexacopter680_flying_arm_2", "hexacopter680_flying_arm_2.urdf"
        )


class HextiltLoader(RobotLoader):
    def __init__(self):
        super().__init__("hextilt", "hextilt.urdf")


class HextiltFlyingArm5Loader(RobotLoader):
    def __init__(self):
        super().__init__("hextilt_flying_arm_5", "hextilt_flying_arm_5.urdf")


ROBOTS = {
    "borinot": BorinotLoader,
    "borinot_flying_arm_2": BorinotFlyingArm2Loader,
    "hexacopter370_flying_arm_3": Hexacopter370FlyingArm3Loader,
    "hexacopter680_flying_arm_2": Hexacopter680FlyingArm2Loader,
    "hextilt": HextiltLoader,
    "hextilt_flying_arm_5": HextiltFlyingArm5Loader,
}


def loader(name, display=False, rootNodeName=""):
    """Load a robot by its name, and optionally display it in a viewer."""
    if name not in ROBOTS:
        robots = ", ".join(sorted(ROBOTS.keys()))
        raise ValueError(
            "Robot '%s' not found. Possible values are %s" % (name, robots)
        )
    inst = ROBOTS[name]()
    if display:
        if rootNodeName:
            inst.robot.initViewer()
            inst.robot.viz.loadViewerModel(rootNodeName=rootNodeName)
        else:
            inst.robot.initViewer(loadModel=True)
        inst.robot.display(inst.robot.q0)
    return inst


def load(name, display=False, rootNodeName=""):
    """Load a robot by its name, and optionally display it in a viewer."""
    return loader(name, display, rootNodeName).robot
