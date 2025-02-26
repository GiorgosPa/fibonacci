from app.fibonacci import config

fibonacci_sequence = [0, 1, 1]


def get_fibonacci_number(n: int) -> int | str:
    return fibonacci_sequence[n]


def compute_fibonacci_number():
    for i in range(3, config.max_number + 1):
        fibonacci_sequence.append(fibonacci_sequence[-1] + fibonacci_sequence[-2])
