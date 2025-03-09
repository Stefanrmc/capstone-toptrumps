import random
import time
from rich import print
animals = ['Cheetah', 'Elephant', 'Owl', 'Dolphin', 'Tiger', 'Gorilla', 'Wolf', 'Crocodile', 'Bald Eagle', 'Grizzly Bear', 'Shark', 'Octopus', 'Snow Leopard',
           'Komodo Dragon', 'Horse', 'Orca']
categories = ['Speed', 'Lifespan', 'Strength', 'Stealth', 'Intelligence']
stats = [[75, 12, 5, 7, 4], [25, 70, 10, 2, 8], [40, 15, 3, 10, 5], [37, 50, 5, 6, 9], [40, 20, 9, 8, 7], [20, 35, 9, 5, 9], [38, 14, 7, 7, 7], [22, 70, 9, 7, 3], [100, 20, 4, 9, 6],
         [35, 25, 10, 5, 6], [35, 70, 9, 8, 5], [25, 10, 3, 9, 10], [40, 15, 7, 10, 6], [12, 30, 8, 6, 4], [55, 30, 6, 4, 5], [34, 50, 10, 7, 9]]

# Making the deck using list comprehension and zip()
pre_deck = [dict(zip(categories, stats[i])) for i in range(len(stats))]

deck = [{animal: stats} for animal, stats in zip(animals, pre_deck)]


def assign_hands(deck):
    '''Returns two lists of 'cards' for the user and computer using random sampling'''
    user_hand = random.sample(deck, k=int(len(deck)/2))
    ai_hand = [x for x in deck if x not in user_hand]
    return user_hand, ai_hand


def flip_coin_to_start():
    '''Simulating a coin flip to return user or AI, for deciding first turn in game.'''
    user_choice = input(
        "A coin flip will decide who gets the first turn. Heads or tails? ").capitalize()
    # Need to validate input!!
    result = random.choice(['Heads', 'Tails'])
    winner = ""
    if result == user_choice:
        winner = "You"
    else:
        winner = "AI"
    time.sleep(0.1)
    print("Coin flipping...")
    time.sleep(1)
    print(f'It is {result}! {winner} will have the first turn!')
    time.sleep(0.5)
    if winner == "You":
        return "user"
    else:
        return "ai"


def active_first_card(hand):
    '''Function to return first card in hand and animal name, for use in other functions for conciseness - when calling function, assign output to variables'''
    for key in hand[0].keys():
        animal = key
    return hand[0], animal


def display_user_card(hand):
    '''Displaying user card'''
    card, animal = active_first_card(hand)
    time.sleep(0.5)
    print(f'\nYour animal is {animal}.\n')
    for category, score in card[animal].items():
        print(f'{category}: {score}')


def user_cat_select(user_hand):
    '''Requesting selected category via validated input and then displaying this selection for user turn'''
    card, animal = active_first_card(user_hand)
    display_user_card(user_hand)

    while True:
        selection = input(
            f'\nWhich category would you like to select? Speed, Lifespan, Strength, Stealth or Intelligence? ').capitalize()
        if selection not in categories:
            print(f'{selection} is not valid! Please select a valid category.')
        else:
            print(f"You chose...")
            print(f"{selection}: {card[animal].get(selection)}")
            return selection


def normalize_card(card, animal, pre_deck):
    '''Changes all category scores for a card to a 1-10 scale, so the AI can suitably select a category'''
    d_normal = {}
    card_normal = {key: value.copy() for key, value in card.items()}
    for category in ['Speed', 'Lifespan']:
        d_normal[f"max_{category}"] = max([d[category] for d in pre_deck])
        d_normal[f"min_{category}"] = min([d[category] for d in pre_deck])
        # Code uses this formula for normalization: x_normalized = a + (((x - x_minimum)*(b - a)) / range of x).
        # Where a is the min of the desired variable range (1-10 here), b is the max of that range and x is the relevant variable.
        card_normal[animal][category] = 1 + (((card[animal][category] - d_normal[f"min_{category}"]) *
                                              (10-1)) / (d_normal[f"max_{category}"] - d_normal[f"min_{category}"]))
    return card_normal[animal]


def ai_cat_select(ai_hand):
    '''Selecting and displaying AI category for AI turn.'''
    # Need to find a way to make sure the computer does not choose the same category twice if there is a tie.
    card, animal = active_first_card(ai_hand)
    normal_stats = normalize_card(card, animal, pre_deck)
    selection = random.choices(
        list(normal_stats.keys()), weights=normal_stats.values(), k=1)[0]
    print(f"AI's card is {animal}")
    time.sleep(1)
    print(f"AI's chosen category is...")
    time.sleep(1)
    print(f"{selection}: {card[animal][selection]}")
    return selection


def turn_winner(category, turn, user_hand, ai_hand):
    '''Use chosen category from previous functions as argument to return the stat of the same category in the waiting player's hand and the leader's hand.
    Function compares scores from each player's active card and determines the winner, moves the cards between hands and returns updated hand plus whose turn follows.'''
    user, ai = 'you', 'AI'
    ai_card, animal_ai = active_first_card(ai_hand)
    u_card, animal_u = active_first_card(user_hand)
    while True:
        if turn == 'user':
            time.sleep(1)
            print(
                f"\nAI's card is {animal_ai} :{animal_ai}:. Its score for {category} is {ai_card[animal_ai].get(category)}.")
            # If the animal does not have an emoji in the rich library, part of this command comes out looking funny. Needs a fix.
        if turn == 'ai':
            time.sleep(1)
            print(
                f"\nYour card is {animal_u} :{animal_u}:. Its score for {category} is {u_card[animal_u].get(category)}.")

        u_score, ai_score = u_card[animal_u].get(
            category), ai_card[animal_ai].get(category)
        if u_score > ai_score:
            time.sleep(2)
            print(f"\n{animal_u} wins! {animal_ai} card goes to {user}!")
            user_hand.append(ai_card)
            ai_hand.remove(ai_card)
            u_card = user_hand.pop(0)
            user_hand.append(u_card)
            turn = 'user'
            time.sleep(2)
            break
        elif ai_score > u_score:
            time.sleep(2)
            print(f"\n{animal_ai} wins! {animal_u} card goes to {ai}!")
            ai_hand.append(u_card)
            user_hand.remove(u_card)
            ai_card = ai_hand.pop(0)
            ai_hand.append(ai_card)
            turn = 'ai'
            time.sleep(4.5)
            break
        else:
            if turn == 'user':
                category = user_cat_select(user_hand)
            if turn == 'ai':
                category = ai_cat_select(ai_hand)
    # This function could definitely be refined - encountered a few bugs so have not been able to make it as concise as would like.
    return turn, user_hand, ai_hand


def gameplay():
    '''Script to run the game, which will end once either the user or computer has run out of cards in their hand.'''
    turn = flip_coin_to_start()
    start_user_hand, start_ai_hand = assign_hands(deck)
    if turn == 'user':
        category = user_cat_select(start_user_hand)
    if turn == 'ai':
        category = ai_cat_select(start_ai_hand)
    turn, new_user_hand, new_ai_hand = turn_winner(
        category, turn, start_user_hand, start_ai_hand)

    while len(new_user_hand) > 0 or len(new_ai_hand) > 0:
        if turn == 'user':
            category = user_cat_select(new_user_hand)
        if turn == 'ai':
            category = ai_cat_select(new_ai_hand)
        turn, new_user_hand, new_ai_hand = turn_winner(
            category, turn, new_user_hand, new_ai_hand)

    if len(new_user_hand) == 0:
        print(f"Oh no, you lose! The AI took all of your cards. Better luck next time!")
    if len(new_ai_hand) == 0:
        print(f"Congratulations, you beat the AI and took all of their cards!")
    # Possible additions: add option to replay, count of number of hands played in a game, no. of hands won.


gameplay()
