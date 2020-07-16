from player import *
from algorithm import *
import sys, getopt


if __name__ == "__main__":
    file = "video/seed720.mp4"
    algorithm = Algorithm()
    player = Player(file, algorithm, sys.argv[1:])
    player.run()
