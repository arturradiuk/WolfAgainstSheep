import playground
import argparse
from configparser import ConfigParser
import logging
import os


def parse_config(file):
    config = ConfigParser()
    config.read(file)
    init = config.get('Terrain', 'InitPosLimit')
    sheep = config.get('Movement', 'SheepMoveDist')
    wolf = config.get('Movement', 'WolfMoveDist')
    if float(init) < 0 or float(sheep) < 0 or float(wolf) < 0:
        logging.error("The numbers in conf file must be positive")
        raise ValueError("Not positive number")
    log = "parse_config(", file, ") called, returned ", float(init), float(sheep), float(wolf)
    logging.debug(log)
    return float(init), float(sheep), float(wolf)


def is_positive(value):
    int_value = int(value)
    if int_value <= 0:
        logging.error("The value must be positive")
        raise argparse.ArgumentTypeError("%s value should be positive" % value)
    log = "is_positive(", value, ") called, returned ", int_value
    logging.debug(log)
    return int_value


init_pos_limit = 10.0
sheep_move_dist = 0.5
wolf_move_dist = 1.0
sheep_number = 15
round_number = 50
wait = False
directory = None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help="configuration file", action='store', dest='conf_file', metavar='FILE')
    parser.add_argument('-d', '--dir', action='store', help="directory to save data", dest='directory',
                        metavar='DIR')
    parser.add_argument('-l', '--log', action='store', help="set log level", dest='log_lvl',
                        metavar='LEVEL')
    parser.add_argument('-r', '--rounds', action='store', help="number of the rounds in simulation", dest='round_no',
                        type=is_positive, metavar='NUM')
    parser.add_argument('-s', '--sheep', action='store',
                        help="number of the sheep in simulation ", dest='sheep_no', type=is_positive,
                        metavar='NUM')
    parser.add_argument('-w', '--wait', action='store_true', help="wait for input after each round")

    args = parser.parse_args()
    if args.directory:
        directory = args.directory
        
    if args.log_lvl:
        if args.log_lvl == "DEBUG":
            lvl = logging.DEBUG
        elif args.log_lvl == "INFO":
            lvl = logging.INFO
        elif args.log_lvl == "WARNING":
            lvl = logging.WARNING
        elif args.log_lvl == "ERROR":
            lvl = logging.ERROR
        elif args.log_lvl == "CRITICAL":
            lvl = logging.CRITICAL
        else:
            raise ValueError("Invalid log level!")

        if directory:
            if not os.path.exists(directory):
                os.mkdir(directory)
            os.chdir(directory)
            logging.basicConfig(level=lvl, filename="chase.log", filemode='w')
            os.chdir("../")
        else:
            logging.basicConfig(level=lvl, filename="chase.log", filemode='w')

    if args.conf_file:
        init_pos_limit, sheep_move_dist, wolf_move_dist, = parse_config(args.conf_file)



    if args.round_no:
        round_number = args.round_no
    if args.sheep_no:
        sheep_number = args.sheep_no
    if args.wait:
        wait = args.wait

    simulation = playground.Simulation(init_pos_limit=init_pos_limit, sheep_move_dist=sheep_move_dist,
                                       wolf_move_dist=wolf_move_dist,
                                       sheep_number=sheep_number, round_number=round_number, directory=directory,
                                       wait=wait)
    simulation.run_rounds()
