# Megamoorecm (A Python Megaman clone)

The goal of this project is to demonstrate a modern development environment, with
clean architecture and sound software engineering practices.  And to do something
fun with it!

## Prerequisites

* bazelisk

## Quickstart

Invoke the game via:
```
bazel run //game:main
```

Run formatting and linting via:
```
bazel run //:buildifier && bazel run //:black
```

Run Tiled (Mac OS), a tile map editor, via:
```
bazel run //:tiled
```

## Documentation

The latest Pygame docs are [here](https://www.pygame.org/docs/).
