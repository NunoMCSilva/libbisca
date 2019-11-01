# TODO: consider this (put inside tests?)
"""
import cProfile
import pstats

from libbisca import RandomAgent, Game


def main():
    agent = RandomAgent()
    print(Game.run_multiple(agents=(agent, agent), num_times=1000))


cProfile.run("main()", ".stats")
pstats.Stats(".stats").sort_stats("tottime").print_stats()
"""
