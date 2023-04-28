load("@pip//:requirements.bzl", "requirement")

py_binary(
    name = "main",
    srcs = [
        "main.py",
    ],
    data = [
        "8bitmegaman.json",
        "@8bitmegaman//file",
    ],
    deps = [
        requirement("pygame"),
    ],
)
