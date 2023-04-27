load("@buildifier_prebuilt//:rules.bzl", "buildifier")
load("@pip//:requirements.bzl", "requirement")

sh_binary(
    name = "tiled",
    srcs = ["wrappers/tiled.sh"],
    data = ["@tiled//:all"],
)

py_binary(
    name = "black",
    srcs = ["wrappers/black-wrapper.py"],
    # The target name "black" conflicts with the Python module, so we have
    # to override the default main to hide the wrapping from the users.
    main = "wrappers/black-wrapper.py",
    deps = [
        requirement("black"),
        requirement("click"),
        requirement("mypy_extensions"),
        requirement("pathspec"),
        requirement("platformdirs"),
        requirement("tomli"),
        requirement("typing_extensions"),
        requirement("packaging"),
    ],
)

buildifier(
    name = "buildifier",
    exclude_patterns = [
        "./.git/*",
    ],
    lint_mode = "fix",
    mode = "fix",
)
