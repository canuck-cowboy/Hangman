from hmwords import choose_hangman
import requests


MAX_CHANCES = 6
API_URL = 'https://api.api-ninjas.com/v1/randomword'
API_KEY = ''


def generate_secret_word():
    try:
        response = requests.get(API_URL, headers={'X-Api-Key': f'{API_KEY}'})
        data = response.json()
        fetched_word = data['word']
        return fetched_word.lower()
    except:
        print('Error fetching word from API')
    return


def prompt():
    while True:
        word = input('Input either a word or a letter to start: ')
        if word.isalpha():
            break
    return word.lower()


def generate_blanks(secret_word):
    temp_answer = ''
    for index in range(0, len(secret_word)):
        temp_answer += '_'
    print(temp_answer)


def initialize():
    print('Start playing Hangman!')
    print(choose_hangman(0))
    generated_secret = generate_secret_word()
    if generated_secret is None:
        print('Terminating Program')
        quit()
    # print(generated_secret)
    generate_blanks(generated_secret)
    return generated_secret


def get_all_indices(letter, word):
    indices = list()
    for index, character in enumerate(word):
        if letter == character:
            indices.append(index)
    return indices


def yes_or_no():
    y_n = input('\nWould you like to have another try?(Y/N) ').lower()
    if y_n in ['y', 'yes', 'yep', 'yup', 'yea', 'yeah', 'sure', 'ok', 'of course', 'ofcourse', 'yepp', 'yeppp', 'yupp',
               'yuppp', 'okk', 'okkk', 'okay', 'ye']:
        y_n = 'y'
    elif y_n in ['n', 'no', 'nop', 'nope', 'nah', 'nopes', 'na']:
        y_n = 'n'
    else:
        print('Invalid input. Game Terminating.')
        quit()
    return y_n


def convert_list_to_string(li):
    my_str = ''.join(li)
    return my_str


def closing_program_statement():
    print('Thanks for playing. Enjoy the rest of your day!')


secret = initialize()
temp_word_list = ['-'] * len(secret)
inserted = list()
chances = 0
# after a game has been initialized, user has only 6 chances
while chances < MAX_CHANCES:
    user_input = prompt()
    # when the user guesses the secret, secret/user input is assigned to the result_string. If user wants to play again,
    # ['-'] * len(secret) is reassigned to temp_word_list. So, here we will also reset the value of result_string.
    # Otherwise, the old secret will be printed rather than ['-'] * len(secret)
    result_string = convert_list_to_string(temp_word_list)
    # if user enters a letter
    if len(user_input) == 1:

        # if letter is in inserted
        if user_input in inserted:
            print('You already used that character', user_input)
            result_string = convert_list_to_string(temp_word_list)

        # if user input doesn't belong to inserted
        else:
            # add it to inserted
            inserted.append(user_input)
            # if letter is in the secret
            if user_input in secret:
                print('Well done,', user_input, 'is correct')
                # get which index or indices the letter is at - update temp_word_list at these indices only
                indices_list = get_all_indices(user_input, secret)
                for i in indices_list:
                    temp_word_list[i] = user_input
                result_string = convert_list_to_string(temp_word_list)

            # if letter is not in the secret
            else:
                print(user_input, 'is incorrect')
                chances += 1

    # if user enters a word
    elif len(user_input) > 1:
        # if the user guesses the word
        if user_input == secret:
            result_string = user_input
        else:
            print('Dont cheat! you can only enter 1 letter')

    # if user doesn't enter anything
    else:
        print('Your selection is not valid.')

    # after processing every user input, print hangman and result_string
    print(choose_hangman(chances))
    print(result_string)

    # if the player used all his tries
    if chances == MAX_CHANCES:
        print(f'Oops, looks like you ran out of tries. The word was {secret}')

    # if the word is guessed
    if result_string == secret:
        print('Well done, you have successfully guessed the word!')

    # if word is guessed or user has used all his tries: check if player wants another round or terminate the program
    if result_string == secret or chances == MAX_CHANCES:
        play_again = yes_or_no()
        # if user wants to play again, reset the secret, chances, and temp_word_list array
        if play_again == 'y':
            secret = initialize()
            inserted.clear()
            chances = 0
            temp_word_list = ['-'] * len(secret)
        # if user doesn't want to play again, break out of the loop
        else:
            closing_program_statement()
            break