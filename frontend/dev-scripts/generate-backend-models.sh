#!/bin/bash
# Note - you need to install openapi-generator-cli first:
# https://openapi-generator.tech/docs/installation/

# Define a function to print a help message
helpFunction() {
    echo ""
    echo "First ensure you have installed openapi-generator-cli: https://openapi-generator.tech/docs/installation/"
    echo "Usage: $0 -o TEMP_OUT_DIR -a BACKEND_API_BASE_PATH"
    echo -e "\t-o Temp directory for the generated models (will be deleted after). Default: temp-out-aiod-models"
    echo -e "\t-a Base directory of the aiod API."
    exit 1 # Exit script after printing help
}

# Get -o and -a arguments from command line
while getopts "o:a:" opt; do
    case "$opt" in
    o) TEMP_OUT_DIR="$OPTARG" ;;
    a) BACKEND_API_BASE_PATH="$OPTARG" ;;
    ?) helpFunction ;; # Print helpFunction in case parameter is non-existent
    esac
done

# Print helpFunction in case mandatory parameters are empty
if [ -z "$BACKEND_API_BASE_PATH" ]; then
    echo "BACKEND_API_BASE_PATH is empty"
    helpFunction
fi

# If BACKEND_API_BASE_PATH ends with /, remove it
if [[ $BACKEND_API_BASE_PATH == */ ]]; then
    BACKEND_API_BASE_PATH=${BACKEND_API_BASE_PATH::-1}
fi

if [ -z "$TEMP_OUT_DIR" ]; then
    TEMP_OUT_DIR="temp-out-backend-models"
fi


# Generate the Python models from the backend API
openapi-generator-cli generate -g typescript-angular --skip-validate-spec --additional-properties=fileNaming=kebab-case -o $TEMP_OUT_DIR -i $BACKEND_API_BASE_PATH/openapi.json

# Copy the typescript models from the $TEMP_OUT_DIR/model directory to
# $SCRIPT_DIR/../src/app/models/backend-generated directory
# Note: the output directory is not created by default, so we need to create it first
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
MODELS_DIR="$SCRIPT_DIR/../src/app/models/backend-generated"
rm -rf $MODELS_DIR
mkdir -p $MODELS_DIR
cp -r $TEMP_OUT_DIR/model/* $MODELS_DIR

# Remove the temporary directory
rm -rf $TEMP_OUT_DIR
