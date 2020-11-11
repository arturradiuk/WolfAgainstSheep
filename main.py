import playground

if __name__ == '__main__':
    simulation = playground.Simulation(sheep_init_pos_limit=10.0, sheep_move_dist=0.5, wolf_move_dist=1.0,
                                       sheep_number=4, round_number=5)
    simulation.run_rounds()


