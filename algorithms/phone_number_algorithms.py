class WrongStartFormat(Exception):
    pass


class WrongBracketFormat(Exception):
    pass


class WrongDashFormat(Exception):
    pass


class WrongLn(Exception):
    pass


class WrongOperator(Exception):
    pass


def correct_start(s):
    if s[:2] == '+7':
        return '+7' + ''.join(s[2:].split())
    elif s[0] == '8':
        return '+7' + ''.join(s[1:].split())
    else:
        raise WrongStartFormat('Неверный формат начала номера')


def correct_oper(s):
    s1 = ''
    for i in s:
        if i not in '()-':
            s1 += i
    number = correct_start(s1)
    chek_cod = int(number[2:5])
    if 910 <= chek_cod <= 919 or 980 <= chek_cod <= 989 or 920 <= chek_cod <= 939 \
            or 902 <= chek_cod <= 906 or 960 <= chek_cod <= 969:
        return True
    else:
        raise WrongOperator('Несуществующий оператор')


def correct_tire(s):
    if s[0] != '-' and s[-1] != '-' and '--' not in s:
        return True
    else:
        raise WrongDashFormat('Неверный формат тире')


def correct_ln(s):
    s1 = ''
    for i in s:
        if i not in '()-':
            s1 += i
    number = correct_start(s1)
    if len(number[1:]) == 11:
        return number
    else:
        raise WrongLn('Неверное количество цифр в номере')


def scobki(s):
    k = 0
    for i in s:
        if i == '(':
            k += 1
        if i == ')':
            k -= 1
        if k >= 2:
            raise WrongBracketFormat('Неверный формат скобок')
        if k < 0:
            raise WrongBracketFormat('Неверный формат скобок')
    if k == 0:
        return True
    else:
        raise WrongBracketFormat('Неверный формат скобок')


def check_phone(string):
    try:
        if scobki(string) and correct_tire(string):
            number = ''
            if correct_start(string):
                for i in correct_start(string):
                    if i in '+0123456789':
                        number += i
                if correct_ln(string):
                    if correct_oper(string):
                        return True,
    except WrongLn as wl:
        return False, wl
    except WrongDashFormat as wd:
        return False, wd
    except WrongBracketFormat as wb:
        return False, wb
    except WrongOperator as wo:
        return False, wo
    except WrongStartFormat as ws:
        return False, ws