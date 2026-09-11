cmake_minimum_required(VERSION 3.22.1)
project(souchastnik)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# llama.cpp is materialized by CI / local bootstrap before CMake starts.
set(LLAMA_CPP_DIR "${CMAKE_SOURCE_DIR}/../../../../third_party/llama.cpp")
if(NOT EXISTS "${LLAMA_CPP_DIR}/CMakeLists.txt")
    message(FATAL_ERROR
        "llama.cpp is missing at ${LLAMA_CPP_DIR}. "
        "Run the repository dependency bootstrap first.")
endif()

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_LIBRARY_OUTPUT_DIRECTORY})

add_subdirectory(${LLAMA_CPP_DIR}
                 ${CMAKE_BINARY_DIR}/llama.cpp
                 EXCLUDE_FROM_ALL)

add_library(souchastnik SHARED llama_bridge.cpp)

target_link_libraries(souchastnik
    llama
    ggml
    android
    log)
