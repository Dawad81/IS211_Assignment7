#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This modal initiates a game of Pig."""

import argparse
import random
random.seed(0)


def new_game():
    """This function initiates a new game of Pig."""
    print
    start = raw_input('Would you like to play a new game of Pig? Enter [y] '
                      'for Yes, or [n] for No:  ')
    if start == 'y':
        dice = Dice()
        player_1 = Player()
        player_2 = Player()
        Game(player_1, player_2, dice)
    elif start == 'n':
        print '-' * 80
        print 'Program exiting......'
        print 'Goodbye!'
        raise SystemExit
    else:
        if start != 'y' or 'n':
            print '-' * 40
            print 'Invalid entry. Please try again'
            print '-' * 40
            new_game()


class Dice(object):
    """This represents the Dice object class."""
    def __init__(self):
        """This is the class constructor for the Dice class."""
        self.value = random.seed(0)

    def roll(self):
        """This represents the result of a roll of the dice."""
        self.value = random.randint(1, 6)


class Player(object):
    """This represents the Player object class."""
    def __init__(self):
        """This is the Player class constructor."""
        self.score = 0
        self.players_turn = False
        self.roll = True
        self.hold = False

    def hold_or_roll(self):
        """This function gives the player a choice, to hold or roll the dice,
        then executes the turn based on the players choice."""
        pick = raw_input(
            '%s: Please enter [h] for Hold, or [r] for Roll? '% self.name)
        pick = str(pick)
        print
        print
        if pick == 'h':
            self.hold = True
            self.roll = False
        elif pick == 'r':
            self.hold = False
            self.roll = True
        else:
            print '*' * 40
            print'Invalid entry. \nPlease try again. \nEnter [h] for Hold ' \
                 'or [r] for Roll. '
            print '*' * 40
            self.hold_or_roll()


class Game(object):
    """This represents the Game object class."""
    def __init__(self, player_1, player_2, dice):
        """This is the Game class constructor, it  initiates the game, and the
        coin toss to select the player who will go first."""
        self.player_1 = player_1
        self.player_1.name = 'Player 1'
        self.player_1.score = 0
        self.player_2 = player_2
        self.player_2.name = 'Player 2'
        self.player_2.score = 0
        self.dice = dice
        self.turn_total = 0
        random.seed(0)
        coin_toss = random.randint(1, 2)
        if coin_toss == 1:
            self.current_player = player_1
            print
            print '***** Player 1 won the coin toss and will go first. *****'
            print
        elif coin_toss == 2:
            self.current_player = player_2
            print
            print '***** Player 2 won the coin toss and will go first. *****'
            print
        self.players_turn()

    def players_turn(self):
        """This function provides the score for the players turn based on the
        results of the hold_or_roll()."""
        print '=' * 25
        print 'Player 1\'s score is:', self.player_1.score
        print 'Player 2\'s score is:', self.player_2.score
        print '=' * 25
        self.dice.roll()
        if self.dice.value == 1:
            print 'The roll resulted in a: 1. Your score is 0.'
            self.turn_total = 0
            self.next_players_turn()
        else:
            self.turn_total = self.turn_total + self.dice.value
            print 'The roll resulted in a:', self.dice.value
            print 'Turn total is:', self.turn_total
            self.current_player.hold_or_roll()
            if self.current_player.hold == True \
                    and self.current_player.roll == False:
                self.current_player.score = self.current_player.score + \
                                            self.turn_total
                self.next_players_turn()
            elif self.current_player.hold == False and \
                    self.current_player.roll == True:
                self.players_turn()

    def next_players_turn(self):
        """This function declares a winner of the game based on the score. If
        there is no winner, it initiates the next players turn."""
        self.turn_total = 0
        if self.player_1.score >= 100:
            print 'Player 1 is the WINNER!'
            print "With a total score of:", self.player_1.score
            self.reset()
            print '-' * 30
            print 'Program exiting......'
            print 'Goodbye!'
        elif self.player_2.score >= 100:
            print 'Player 2 is the WINNER!'
            print 'With a total score of:', self.player_2.score
            self.reset()
            print '-' * 30
            print 'Program exiting......'
            print 'Goodbye!'
        else:
            if self.current_player == self.player_1:
                self.current_player = self.player_2
            elif self.current_player == self.player_2:
                self.current_player = self.player_1
            print
            print 'Next players turn. Roll is now on', self.current_player.name
            print
            self.players_turn()

    def reset(self):
        """This function resets the game after a winner has been declared."""
        self.turn_total = None
        self.player_1 = None
        self.player_2 = None
        self.dice = None


def matchmaking(players=list, teams=int, min_team=2, max_team=2):
    """This function matches the number of players entered in --numPlayers,
    in to random groups of 2, to play individual games of Pig against one
    another."""
    factor = len(players) / (teams * min_team * 1.0)
    if factor < 1:
        return False
    else:
        if max_team is not None and len(players) > (teams * max_team):
            players = players[:(teams * max_team)]
        game = []
        for i in range(teams):
            teamlist = players[i::teams]
            game.append(teamlist)
    return game

def main():
    """This function initiates the game of Pig, with multiple players, in
    multiple games, via the comand line with the --numPlayers argument.
    Additionaly, if no --numPlayer is enterd it will automaticly prompt to ask
    if you want to begin a game of Pig with just 2 players."""
    parser = argparse.ArgumentParser()

    parser.add_argument("--numPlayers",
                        help="Enter the number of players.(optional)",
                        required=False, type=int)
    args = parser.parse_args()
    try:
        if args.numPlayers:
            print 'number of players = ', args.numPlayers
            player_l = []
            for x in range(args.numPlayers):
                player_l.append('Player ')
            counter = 0
            players_list = []
            for num, player in enumerate(player_l):
                players = player + str(num)
                players_list.append(players)
                counter += 1
            if len(players_list) % 2 != 0:
                print "--numPlayers must be an even number!"
                print '-' * 80
                print 'Program exiting......'
                print 'Goodbye!'
                raise SystemExit
            else:
                team = int(len(players_list) /2)
                games = matchmaking(players_list, team)
                for num, item in enumerate(games):
                    print '-' * 47
                    print 'Game {}: Will be between {} and {}.'.format(
                        num, item[0], item[1])
                    print '-' * 47
                for item in games:
                    print
                    print '=*'*24
                    print 'This is the game between {} and {}'.format(
                        item[0], item[1])
                    print
                    print '{} will be Player 1'.format(item[0])
                    print '{} will be Player 2'.format(item[1])
                    print
                    print '=*' * 24
                    item[0] = Player()
                    item[1] = Player()
                    dice = Dice()
                    Game(item[0], item[1], dice)
        else:
            new_game()
    except:
        print
        print '*' * 80
        print 'An error has occured session terminated.\n\
            Exiting the program......Good Bye.'
        print '*' * 80
        print
        SystemExit


if __name__ == '__main__':
    main()
