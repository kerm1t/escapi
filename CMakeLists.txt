cmake_minimum_required(VERSION 3.0)
set(CMAKE_FIND_PACKAGE_PREFER_CONFIG ON)

project(webcam)

#set(CMAKE_BUILD_TYPE "Release")
#set(CMAKE_CXX_FLAGS "-std=c++14")
#set(CMAKE_CXX_FLAGS_RELEASE "-O3 -Wall -g")

#set(CMAKE_CXX_STANDARD 14)
#set(CMAKE_CXX_STANDARD_REQUIRED ON)

if (MSVC)
  set(CMAKE_CXX_STANDARD 11)             # needed for eCAL
  set(CMAKE_CXX_STANDARD_REQUIRED ON)    # needed for eCAL
endif()

# find packages and ... a bit ugly ... set directories by hand, all lib-packages are in c:\lib

set (SDL2_DIR C:/lib/SDL2-2.30.11/cmake)
find_package(SDL2 REQUIRED)
find_package(OpenGL REQUIRED)

# hmmm, eCAL build stopped working --> zlib installed from https://gnuwin32.sourceforge.net/packages/zlib.htm --> Complete package
set(ZLIB_LIBRARY C:/lib/zlib/lib)
set(ZLIB_INCLUDE_DIR C:/lib/zlib/include)

find_package(eCAL REQUIRED)
find_package(Protobuf REQUIRED)


include_directories(
#  include
  common
  ${SDL2_INCLUDE_DIRS}
  ${OPENGL_INCLUDE_DIRS} // needed by SDL
)

#link_directories(
#  include
#)

# eCAL / proto
set(protobuf_files
    ${CMAKE_CURRENT_SOURCE_DIR}/proto/webcam.proto
)
add_executable(${PROJECT_NAME} ogl_eCAL/main.cpp common/escapi.cpp)

# compile protos
PROTOBUF_TARGET_CPP(${PROJECT_NAME} ${CMAKE_CURRENT_SOURCE_DIR}/proto/ ${protobuf_files})


target_link_libraries(${PROJECT_NAME} ${SDL2_LIBRARIES} ${OPENGL_LIBRARIES} eCAL::core protobuf::libprotobuf)