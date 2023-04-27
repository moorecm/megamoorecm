import black
import os
import pathlib
import sys

if __name__ == "__main__":
    workspace = pathlib.Path(os.environ["BUILD_WORKSPACE_DIRECTORY"])
    sys.exit(black.main(["--verbose"] + [str(p) for p in workspace.rglob("*.py")]))
