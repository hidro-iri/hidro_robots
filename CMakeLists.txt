cmake_minimum_required(VERSION 3.8)
project(hidro_robots)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(xacro)

option(CREATE_PLAIN_URDFS "Create plain udrfs from description files" OFF)

if(CREATE_PLAIN_URDFS)
  if(xacro_FOUND)
    message(STATUS "Creating plain URDFs")

    file(GLOB ROBOTS_DIR "${CMAKE_SOURCE_DIR}/robots/*")
    foreach(ROBOT_DIR ${ROBOTS_DIR})
      get_filename_component(ROBOT_NAME ${ROBOT_DIR} NAME)
      if(EXISTS "${ROBOT_DIR}/xacro/description.urdf.xacro")
        message(STATUS "   Creating " ${ROBOT_NAME})
        execute_process(
          COMMAND xacro ${ROBOT_DIR}/xacro/description.urdf.xacro -o
                  ${ROBOT_DIR}/${ROBOT_NAME}.urdf simulation:=false)
      endif()
    endforeach()
  endif()
endif()

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights uncomment
  # the line when a copyright and license is not present in all source files
  # set(ament_cmake_copyright_FOUND TRUE) the following line skips cpplint (only
  # works in a git repo) uncomment the line when this package is not in a git
  # repo set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

install(DIRECTORY robots DESTINATION share/${PROJECT_NAME}/)
install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})
install(DIRECTORY worlds DESTINATION share/${PROJECT_NAME})

ament_package()
