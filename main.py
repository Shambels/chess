from functools import lru_cache
from pathlib import Path

from abc import ABC

from chess import Game


def main() -> None:
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
