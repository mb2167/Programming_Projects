#pragma once
#include <string>
#include <filesystem>

inline std::string getOutputDir() {
    return std::string(PROJECT_ROOT_DIR) + "/output";
}

