from random import choice
import sys
from os.path import exists
from urllib.request import urlopen

MIN_ARGC = 2


def bullscows(guess: str, secret: str) -> (int, int):
    return (len([i for i in range(min(len(guess), len(secret))) if guess[i] == secret[i]]),
            len([x for x in guess if x in secret]))


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    if words == []:
        raise ValueError("Произошла ошибка (задан пустой словарь)")

    secret = choice(words)
    attempts_n = 0

    while (guess := ask("Введите слово: ", words)) != secret:
        inform("Быки: {}, Коровы: {}", *bullscows(guess, secret))
        attempts_n += 1

    return attempts_n + 1


def ask(prompt: str, valid: list[str] = None) -> str:
    if valid is None:
        return input(prompt)
    else:
        while (guess := input(prompt)) not in valid:
            print("Ввод недопустим (неизвестное слово)")

        return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


def main(length: int = 5) -> None:
    if len(sys.argv) < MIN_ARGC:
        print("Usage: python -m bullscows словарь\nor\npython -m bullscows словарь длина")
        return

    if exists(sys.argv[1]):
        with open(sys.argv[1], "r") as f:
            d = f.read().split()
    else:
        try:
            d = urlopen(sys.argv[1]).read().decode().split()
        except Exception:
            raise ValueError("Произошла ошибка (словарь не распознан)")

    if len(sys.argv) > MIN_ARGC:
        try:
            length = int(sys.argv[2])
        except Exception:
            raise ValueError("Произошла ошибка (неверный формат длины)")

    d = [wd for wd in d if len(wd) == length]

    print(f"Вы угадали слово! Количество попыток: {gameplay(ask, inform, d)}")


if __name__ == "__main__":
    main()
