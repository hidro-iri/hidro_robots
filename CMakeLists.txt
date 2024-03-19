cmake_minimum_required(VERSION 3.8)
project(hidro_robots)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

option(CREATE_PLAIN_URDFS "Create plain udrfs from description files" OFF)

if(CREATE_PLAIN_URDFS)
  find_package(xacro)
  if(xacro_FOUND)
    message(STATUS "Creating plain URDFs")

    file(GLOB ROBOTS_DIR "${CMAKE_SOURCE_DIR}/robots/*")
    foreach(ROBOT_DIR ${ROBOTS_DIR})
      get_filename_component(ROBOT_NAME ${ROBOT_DIR} NAME)
      if(EXISTS "${ROBOT_DIR}/xacro/description.urdf.xacro")
        message(STATUS "   Creating " ${ROBOT_NAME})
        execute_process(
          COMMAND xacro ${ROBOT_DIR}/xacro/description.urdf.xacro -o
                  ${ROBOT_DIR}/${ROBOT_NAME}.urdf simulation:=false event_based_sim:=false)
      endif()
    endforeach()
  else()
    message(
      FATAL_ERROR
        "To create the URDFs you must source the ROS installation with the XACRO package installed"
    )
  endif()
endif()

find_package(ament_cmake QUIET)

configure_file(
  ${hidro_robots_SOURCE_DIR}/cmake/hidro_robots-config.cmake.in
  ${hidro_robots_BINARY_DIR}/cmake/${PROJECT_NAME}-config.cmake @ONLY)
configure_file(${hidro_robots_SOURCE_DIR}/config/path.py.in
               ${hidro_robots_BINARY_DIR}/python/path.py @ONLY)

install(DIRECTORY robots DESTINATION share/${PROJECT_NAME})
install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})
install(DIRECTORY worlds DESTINATION share/${PROJECT_NAME})
install(FILES ${hidro_robots_BINARY_DIR}/cmake/${PROJECT_NAME}-config.cmake
        DESTINATION lib/cmake/${PROJECT_NAME})

# PYTHON LIBRARIES
find_package(Python3 REQUIRED COMPONENTS Development)
install(
  DIRECTORY python/hidro_robots
  DESTINATION
    lib/python${Python3_VERSION_MAJOR}.${Python3_VERSION_MINOR}/dist-packages)
install(
  FILES ${hidro_robots_BINARY_DIR}/python/path.py
  DESTINATION
    lib/python${Python3_VERSION_MAJOR}.${Python3_VERSION_MINOR}/dist-packages/${PROJECT_NAME}
)

if(NOT TARGET uninstall)
  configure_file(
    "${hidro_robots_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake" IMMEDIATE @ONLY)

  add_custom_target(
    uninstall COMMAND ${CMAKE_COMMAND} -P
                      ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake)
endif()

if(${ament_cmake_FOUND})
  message(WARNING "Calling ament package")
  ament_package()
endif()
