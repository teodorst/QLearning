from argparse import ArgumentParser
from matplotlib import pyplot as plt
import numpy as np
import sys
from random import choice
from time import sleep

from game import Game


def q_learning(args):
    game = Game(args.map_file, args.radius)

    Q = {}
    scores = []
    eval_scores = []
    for train_ep in range(args.train_episodes):
        game.reset_game()
        score = 0
        pas = 0
        while pas < args.max_moves and not game.is_final_state():
            state = game.serialize_state()
            # action = choice(game.get_legal_actions())
            # action = game.best_action(Q, state, game.get_legal_actions())
            action = game.epsilon_greedy(Q, state, game.get_legal_actions(), 0.05)

            if (state, action) not in Q:
                Q[(state, action)] = 0

            new_state, reward = game.game_move(action)
            best_val = -sys.maxint
            new_actions = game.get_legal_actions()

            for new_action in new_actions:
                if (new_state, new_action) not in Q:
                    Q[(new_state, new_action)] = 0
                if Q[(new_state, new_action)] > best_val:
                    best_val = Q[(new_state, new_action)]

            Q[(state, action)] = Q[(state, action)] + args.learning_rate * (
                reward + args.discount * best_val - Q[(state, action)])

            score += reward
            pas += 1
        print 'Episode %6d / %6d' % (train_ep, args.train_episodes)
        scores.append(score)

        if train_ep % args.eval_every == 0:
            avg_score = .0

            for _ in range(args.eval_episodes):
                eval_final_score = 0
                pas = 0
                game.reset_game()
                while pas < args.max_moves and not game.is_final_state():
                    state = game.serialize_state()
                    # action = choice(game.get_legal_actions())
                    # action = game.best_action(Q, state, game.get_legal_actions())
                    action = game.epsilon_greedy(Q, state, game.get_legal_actions(), 0.05)
                    new_state, reward = game.game_move(action)
                    eval_final_score += reward
                    pas += 1
                avg_score += eval_final_score

            avg_score = float(avg_score) / args.eval_episodes
            eval_scores.append(avg_score)

    if args.final_show:
        game.reset_game()
        score = 0
        while pas < args.max_moves and not game.is_final_state():
            state = game.serialize_state()
            # action = choice(game.get_legal_actions())
            # action = game.best_action(Q, state, game.get_legal_actions())
            action = game.epsilon_greedy(Q, state, game.get_legal_actions(), 0.05)
            new_state, reward = game.game_move(action)
            print action, reward
            _, _des_state = game.deserialize_state(new_state)
            for h in _des_state:
                print h
            print ''
            sleep(args.sleep_time)
            score += reward
        if game.current_pos == game.finish_pos:
            print "You win %d " % score
        else:
            print "You lost %d " % score

    return Q, scores, eval_scores


def generate_plot(args, train_scores, eval_scores):
    plt.xlabel("Episode")
    plt.ylabel("Average score")
    plt.plot(
        np.linspace(1, args.train_episodes, args.train_episodes),
        np.convolve(train_scores, [0.2, 0.2, 0.2, 0.2, 0.2], "same"),
        linewidth=1.0, color="blue"
    )
    plt.plot(
        np.linspace(args.eval_every, args.train_episodes, len(eval_scores)),
        eval_scores, linewidth=2.0, color="red"
    )
    plt.show()

if __name__ == "__main__":
    parser = ArgumentParser()
    # Input file
    parser.add_argument("--map_file", type=str, default="test.txt",
                        help="File to read map from.")
    # Meta-parameters
    parser.add_argument("--learning_rate", type=float, default=0.1,
                        help="Learning rate")
    parser.add_argument("--discount", type=float, default=0.99,
                        help="Value for the discount factor")
    parser.add_argument("--epsilon", type=float, default=0.05,
                        help="Probability to choose a random action.")
    parser.add_argument("--max_moves", dest="max_moves",
                        type=int,
                        default=1000,
                        help="Max moves per game.")
    parser.add_argument("--radius", type=int, default=4,
                        help="H's sight radius.")
    # Training and evaluation episodes
    parser.add_argument("--train_episodes", type=int, default=1000,
                        help="Number of episodes")

    parser.add_argument("--eval_every", type=int, default=10,
                        help="Evaluate policy every ... games.")

    parser.add_argument("--eval_episodes", type=int, default=10,
                        help="Number of games to play for evaluation.")
    # Display
    parser.add_argument("--verbose", dest="verbose",
                        action="store_true", help="Print each state")
    parser.add_argument("--plot", dest="plot_scores", action="store_true",
                        help="Plot scores in the end")
    parser.add_argument("--final_show", dest="final_show",
                        action="store_true",
                        help="Demonstrate final strategy.")
    parser.add_argument("--sleep_time", type=float, default=0.2,
                        help="Time between moves.")

    args = parser.parse_args()
    final_Q, results, eval_results = q_learning(args)
    if args.plot_scores:
        generate_plot(args, results, eval_results)



