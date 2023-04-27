import sys

import engine


def main():
    game = engine.Engine()
    game.loop()


if __name__ == "__main__":
    print(f"Python {sys.version}")
    sys.exit(main())
