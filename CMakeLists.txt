cmake_minimum_required(VERSION 3.20)

project(MCPGatewayDashboard LANGUAGES NONE)

include(CTest)

option(
    MCP_GATEWAY_SETUP_TEST_ENV
    "Create an isolated Python virtual environment and install test dependencies"
    ON
)

if(BUILD_TESTING)
    find_package(Python3 3.9 REQUIRED COMPONENTS Interpreter)

    set(MCP_GATEWAY_TEST_PYTHON "${Python3_EXECUTABLE}")

    if(MCP_GATEWAY_SETUP_TEST_ENV)
        set(MCP_GATEWAY_TEST_VENV "${CMAKE_BINARY_DIR}/test-venv")

        if(WIN32)
            set(MCP_GATEWAY_TEST_PYTHON "${MCP_GATEWAY_TEST_VENV}/Scripts/python.exe")
        else()
            set(MCP_GATEWAY_TEST_PYTHON "${MCP_GATEWAY_TEST_VENV}/bin/python")
        endif()

        if(NOT EXISTS "${MCP_GATEWAY_TEST_PYTHON}")
            message(STATUS "Creating isolated test environment: ${MCP_GATEWAY_TEST_VENV}")
            execute_process(
                COMMAND "${Python3_EXECUTABLE}" -m venv "${MCP_GATEWAY_TEST_VENV}"
                RESULT_VARIABLE venv_result
                ERROR_VARIABLE venv_error
            )
            if(NOT venv_result EQUAL 0)
                message(FATAL_ERROR "Failed to create the test environment: ${venv_error}")
            endif()
        endif()

        message(STATUS "Installing test dependencies from requirements.txt")
        execute_process(
            COMMAND
                "${MCP_GATEWAY_TEST_PYTHON}" -m pip install
                --disable-pip-version-check
                -r "${CMAKE_SOURCE_DIR}/requirements.txt"
            RESULT_VARIABLE pip_result
            ERROR_VARIABLE pip_error
        )
        if(NOT pip_result EQUAL 0)
            message(FATAL_ERROR "Failed to install test dependencies: ${pip_error}")
        endif()
    endif()

    add_test(
        NAME dashboard.unit
        COMMAND
            "${MCP_GATEWAY_TEST_PYTHON}" -m unittest
            discover -s "${CMAKE_SOURCE_DIR}/tests" -v
        WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
    )

    set_tests_properties(
        dashboard.unit
        PROPERTIES
            LABELS "dashboard;unit;flask"
            ENVIRONMENT "PYTHONPATH=${CMAKE_SOURCE_DIR}"
    )

    add_custom_target(
        test-pack
        COMMAND
            "${CMAKE_CTEST_COMMAND}"
            --test-dir "${CMAKE_BINARY_DIR}"
            --build-config "$<CONFIG>"
            --output-on-failure
        COMMENT "Running the MCP Gateway dashboard test pack"
        USES_TERMINAL
    )
endif()
