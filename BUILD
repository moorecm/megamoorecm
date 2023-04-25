load("@buildifier_prebuilt//:rules.bzl", "buildifier")
load("@pip//:requirements.bzl", "requirement")

py_binary(
    name = "main",
    srcs = ["main.py"],
    deps = [
        requirement("pygame"),
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
