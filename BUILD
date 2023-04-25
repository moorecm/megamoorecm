load("@buildifier_prebuilt//:rules.bzl", "buildifier")
load("@pip//:requirements.bzl", "requirement")

py_binary(
    name = "main",
    srcs = [
        "main.py",
    ],
    data = [
        "@8bitmegaman//file",
    ],
    deps = [
        requirement("pygame"),
    ],
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
