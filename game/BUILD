load("@pip//:requirements.bzl", "requirement")

py_binary(
    name = "main",
    srcs = [
        "main.py",
    ],
    data = [
        "8bitmegaman.json",
        "@8bitmegaman//file",
        "@smb//file",
    ],
    deps = [
        ":level",
        requirement("pygame"),
    ],
)

py_library(
    name = "level",
    srcs = ["level.py"],
    data = [
        "level1.tmx",
        "smb.tsx",
        "@smb//file",
    ],
    visibility = [
        ":__pkg__",
        "//:__pkg__",
    ],
    deps = [
        requirement("pygame"),
        requirement("pytmx"),
    ],
)
