#!/bin/bash

# This is a hack to allow Tiled and //game:main to both use the same relative paths to find resources.
ln -sf bazel-bin/tiled.runfiles/_main/external $BUILD_WORKSPACE_DIRECTORY/external

"$BUILD_WORKSPACE_DIRECTORY/bazel-megamoorecm/external/tiled/Tiled.app/Contents/MacOS/Tiled" "$@"

rm -f $BUILD_WORKSPACE_DIRECTORY/external
