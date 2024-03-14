#!/bin/bash
# Note - you need to install datamodel-codegen first:
# https://docs.pydantic.dev/latest/integrations/datamodel_code_generator/
# pip install datamodel-code-generator

# Define a function to print a help message
helpFunction() {
    echo ""
    echo "First ensure you have installed datamodel-codegen: pip install datamodel-code-generator"
    echo "Usage: $0 -o TEMP_OUT_DIR -a AIOD_API_BASE_PATH"
    echo -e "\t-o Temp directory for the generated models (will be deleted after). Default: temp-out-aiod-models"
    echo -e "\t-a Base directory of the aiod API."
    exit 1 # Exit script after printing help
}

# Get -o and -a arguments from command line
while getopts "o:a:" opt; do
    case "$opt" in
    o) TEMP_OUT_DIR="$OPTARG" ;;
    a) AIOD_API_BASE_PATH="$OPTARG" ;;
    ?) helpFunction ;; # Print helpFunction in case parameter is non-existent
    esac
done

# Print helpFunction in case mandatory parameters are empty
if [ -z "$AIOD_API_BASE_PATH" ]; then
    echo "AIOD_API_BASE_PATH is empty"
    helpFunction
fi

# If AIOD_API_BASE_PATH ends with /, remove it
if [[ $AIOD_API_BASE_PATH == */ ]]; then
    AIOD_API_BASE_PATH=${AIOD_API_BASE_PATH::-1}
fi

if [ -z "$TEMP_OUT_DIR" ]; then
    TEMP_OUT_DIR="temp-out-aiod-models"
fi

# Generate Pydantic models from aiod API
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
MODELS_DIR="$SCRIPT_DIR/../app/schemas"

mkdir $TEMP_OUT_DIR
wget "$AIOD_API_BASE_PATH/openapi.json" -O "$TEMP_OUT_DIR/openapi.json"
datamodel-codegen --input "$TEMP_OUT_DIR/openapi.json" --input-file-type openapi --output "$MODELS_DIR/aiod_generated.py"

# Remove the temporary directory
rm -rf $TEMP_OUT_DIR
