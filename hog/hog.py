"""CS 61A Presents The Game of Hog."""

from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    pig = False 
    roll_sum = 0
    while num_rolls>0:
        temp = dice()
        num_rolls -= 1
        if (temp == 1):
            pig = True
        else: 
            roll_sum += temp
    if pig:
        return 1
    else:  
        return roll_sum      
    # END PROBLEM 1


def free_bacon(score):
    """Return the points scored from rolling 0 dice (Free Bacon).

    score:  The opponent's current score.
    """
    assert score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    num = pow(score,3)
    even = 0
    odd = 0
    i = 0
    total = 0
    while num > 0:
        
        if (i+1)%2 == 0:
            even += num%10
        else:
            odd += num%10
        i+=1
        num //= 10
        
    total = 1 + abs(even - odd)
    return total
    # END PROBLEM 2


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 3
    if num_rolls == 0:
        return free_bacon(opponent_score)
    else: 
        return roll_dice(num_rolls, dice)
    # END PROBLEM 3


def is_swap(player_score, opponent_score):
    """
    Return whether the two scores should be swapped
    """
    # BEGIN PROBLEM 4
    num = 3**(player_score + opponent_score)
    if int(str(num)[:1]) == num%10:
        return True
    else:
        return False
    # END PROBLEM 4


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who


def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    print(score0, score1)
    return silence


#AssertionError: num_rolls must be an integer. Because the strategy function has not implemented and would be mentioned in phase 3
def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence, feral_hogs=True):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    feral_hogs: A boolean indicating whether the feral hogs rule should be active.
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    current_score0, current_score1 = 0, 0
    pre_score0, pre_score1 = 0, 0
    while score0<goal and score1<goal:
        if who == 0:
            num_roll0 = strategy0(score0, score1)
            current_score0 = take_turn(num_roll0, score1, dice)
            score0 += current_score0
        elif who == 1:
            num_roll1 = strategy1(score1, score0)
            current_score1 = take_turn(num_roll1, score0, dice)
            score1 += current_score1
            
        if feral_hogs:
            if who == 0 and abs(num_roll0 - pre_score0) == 2:
                score0 += 3
            elif who == 1 and abs(num_roll1 - pre_score1) == 2:
                score1 += 3
            pre_score0 = current_score0
            pre_score1 = current_score1
                
        if is_swap(score0, score1):
            score0, score1 = score1, score0
        who = other(who) #change to the other one
        say = say(score0, score1)
#         announce = announce_highest(who, prev_high, prev_score)
    return score0, score1


#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores

def announce_lead_changes(prev_leader=None):
    """Return a commentary function that announces lead changes.

    >>> f0 = announce_lead_changes()
    >>> f1 = f0(5, 0)
    Player 0 takes the lead by 5
    >>> f2 = f1(5, 12)
    Player 1 takes the lead by 7
    >>> f3 = f2(8, 12)
    >>> f4 = f3(8, 13)
    >>> f5 = f4(15, 13)
    Player 0 takes the lead by 2
    """
    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != prev_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)
    return say

def both(f, g):
    """Return a commentary function that says what f says, then what g says.

    NOTE: the following game is not possible under the rules, it's just
    an example for the sake of the doctest

    >>> h0 = both(say_scores, announce_lead_changes())
    >>> h1 = h0(10, 0)
    Player 0 now has 10 and Player 1 now has 0
    Player 0 takes the lead by 10
    >>> h2 = h1(10, 6)
    Player 0 now has 10 and Player 1 now has 6
    >>> h3 = h2(6, 17)
    Player 0 now has 6 and Player 1 now has 17
    Player 1 takes the lead by 11
    """
    def say(score0, score1):
        return both(f(score0, score1), g(score0, score1))
    return say


def announce_highest(who, prev_high=0, prev_score=0):
    """Return a commentary function that announces when WHO's score
    increases by more than ever before in the game.

    NOTE: the following game is not possible under the rules, it's just
    an example for the sake of the doctest

    >>> f0 = announce_highest(1) # Only announce Player 1 score gains
    >>> f1 = f0(12, 0)
    >>> f2 = f1(12, 11)
    11 point(s)! That's the biggest gain yet for Player 1
    >>> f3 = f2(20, 11)
    >>> f4 = f3(13, 20)
    >>> f5 = f4(20, 35)
    15 point(s)! That's the biggest gain yet for Player 1
    >>> f6 = f5(20, 47) # Player 1 gets 12 points; not enough for a new high
    >>> f7 = f6(21, 47)
    >>> f8 = f7(21, 77)
    30 point(s)! That's the biggest gain yet for Player 1
    >>> f9 = f8(77, 22) # Swap!
    >>> f10 = f9(33, 77) # Swap!
    55 point(s)! That's the biggest gain yet for Player 1
    """
    assert who == 0 or who == 1, 'The who argument should indicate a player.'
    # BEGIN PROBLEM 7
    def say(score0, score1):
        if who == 0:
            current_score = score0
        elif who == 1:
            current_score = score1
            
        diff = current_score - prev_score
        if diff > prev_high:
            print (str(diff), "point(s)! That's the biggest gain yet for Player", str(who))
            return announce_highest(who, diff, current_score) #update the pre high
        else:
            return announce_highest(who, prev_high, current_score) #no update
    return say
        # END PROBLEM 7


#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def make_averaged(g, num_samples=1000):
    """Return a function that returns the average value of G when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    """
    # BEGIN PROBLEM 8
    def sub_averaged(*args):
        result = 0
        k = 1
        while k <= num_samples: 
            result += g(*args)
            k += 1
        return result/num_samples
    return sub_averaged
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
#     average_score = 0
#     num_dice = 10
#     result = 0
    
#     #only one num_dice in the function
#     num_of_dice = roll_dice(num_dice)
#     first_digit = dice
#     if first_digit == 1:
#         return 1
#     elif num_of_dice == 1:
#         return 10
#     return average_score
    
#     while num_dice > 0:
#         average_score = make_averaged(roll_dice, num_samples)(num_dice, dice)
#         result = max(result, average_score)
#         if average_score >= result:
#             average_score = num_dice
#         num_dice -= 1
#     return average_score
         
    max_score = 0
    max_num = 0
    for num_rolls in range(1, 11):
        average_dice = make_averaged(roll_dice, num_samples)
        current_score = average_dice(num_rolls, dice)
        if current_score > max_score:
            max_num = num_rolls
            max_score = current_score
    return max_num
        
#     if average_score == 1:
#         return 1
#     elif num_rolls == 1:
#         return 10
#     else:
#         return average_score
        
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if False:  # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"



def bacon_strategy(score, opponent_score, margin=8, num_rolls=6):
    """This strategy rolls 0 dice if that gives at least MARGIN points, and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    bacon_score = free_bacon(opponent_score)
    if bacon_score >= margin:
        return 0
    else:
        return num_rolls
    # END PROBLEM 10


def swap_strategy(score, opponent_score, margin=8, num_rolls=6):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points and does not trigger a
    non-beneficial swap. Otherwise, it rolls NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    bacon_score = free_bacon(opponent_score) 
    new_score = score + bacon_score
    if is_swap(new_score, opponent_score) and (opponent_score > new_score):
        return 0
    elif is_swap(new_score, opponent_score) and (opponent_score < new_score):
        return num_rolls
    elif (bacon_score >= margin) or (is_swap(new_score, opponent_score) and (opponent_score == new_score)):
        return 0
    else:
        return num_rolls
    
    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    return 4
#     dice = roll_dice(score, opponent_score)
#     free_bacon = take_turn(0, opponent_score)

#     #Make swap :
#     if is_swap(score + 1, opponent_score) and ((score + 1) < opponent_score):
#         return 10

#     if is_swap(score + free_bacon, opponent_score) and ((score + free_bacon) < opponent_score):
#         return 0

#     #Make opponent 4_sided_dice (Hogwild):
#     if (score + free_bacon + opponent_score) % 7 == 0 and free_bacon > 4:
#         return 0

#     #More general rules:
#     if score < 65 and opponent_score > 79:
#         if dice == four_sided:
#             return bacon_strategy(score, opponent_score, 5, 2)
#         else:
#             return 10

#     if score - opponent_score > 33:
#         if dice == four_sided:
#             return 3
#         else:
#             return bacon_strategy(score, opponent_score, 9, 4)

#     if opponent_score - score > 40:
#         if dice == four_sided:
#             return bacon_strategy(score, opponent_score, 8, 4)
#         else:
#             return 8

#     if opponent_score - score > 16:
#         if dice == four_sided:
#             return bacon_strategy(score, opponent_score, 2, 5)
#         else:
#             return 8

#     if score > 82:
#         if dice == four_sided:
#             return bacon_strategy(score, opponent_score, 4, 10)
#         else:
#             return bacon_strategy(score, opponent_score, 7, 2)

#     if score > opponent_score:
#         if ((score + 1 + opponent_score) % 7) == 0:
#             return 5
#         if dice == four_sided:
#             return bacon_strategy(score, opponent_score, 5, 3)
#         else:
#             return bacon_strategy(score, opponent_score, 9, 5)

#     if score < opponent_score:
#         if ((score + 1 + opponent_score) % 7) == 0:
#             return 7
#         if dice == four_sided:
#             return bacon_strategy(score, opponent_score, 5, 5)
#         else:
#             return bacon_strategy(score, opponent_score, 10, 6)

#     if dice == four_sided:
#         return bacon_strategy(score, opponent_score, 4, 5)
#     else:
#         return bacon_strategy(score, opponent_score, 10, 6)
    # END PROBLEM 12

##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()