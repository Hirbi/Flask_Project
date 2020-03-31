def min_password_length(string):
    return len(string) >= 8


def english_letters_only(string):
    letters = 'QWERTYUIOPASDFGHJKLZXCVBNM1234567890_'
    for letter in string:
        if letter not in letters and letter not in letters.lower():
            return False
    return True


def big_letter_required(string):
    letters = 'QWERTYUIOPASDFGHJKLZXCVBNM'
    for letter in string:
        if letter in letters:
            return True
    return False


def small_letter_required(string):
    letters = 'QWERTYUIOPASDFGHJKLZXCVBNM'.lower()
    for letter in string:
        if letter in letters:
            return True
    return False


def num_required(string):
    letters = '1234567890'
    k = 0
    for letter in string:
        if letter in letters:
            k += 1
    return k >= 3


def low_space_required(string):
    for letter in string:
        if letter == '_':
            return True
    return False


def same_letters_in_a_row_prohibited(string):
    k = 0
    previous = ''
    for letter in string:
        if letter == previous:
            k += 1
            if k >= 4:
                return False
        previous = letter
    return True


def chek_password_combination(string):
    return min_password_length(string) and english_letters_only(string) and\
           big_letter_required(string) and small_letter_required(string) and\
           num_required(string) and low_space_required(string) and\
           same_letters_in_a_row_prohibited(string)
