from pydantic import BaseModel, field_validator, model_validator

from app.fibonacci import config


fibonacci_sequence = [0, 1, 1]


class Fibonacci(BaseModel):
    index: int
    number: int | float | str

    @field_validator('number', mode='before')
    @classmethod
    def check_number(cls, value: int | float) -> int | float | str:
        if value > config.max_float:
            return str(value)
        return value


class FibonacciList(BaseModel):
    page: int
    limit: int = 100
    fibonacci_numbers: list[Fibonacci]

    @field_validator('limit', mode='before')
    @classmethod
    def check_max_limit(cls, value: int) -> str:
        if value > config.max_numbers_per_page:
            raise ValueError(f"Limit must be less than or equal to {config.max_numbers_per_page}")
        return value

    @model_validator(mode='before')
    @classmethod
    def check_page_and_limit(cls, data: dict) -> str:
        max_page = config.max_number // data['limit'] + 1
        if data['page'] > max_page:
            raise ValueError(f"Page {data['page']} does not exist. For limit: {data['limit']} last page is {max_page}")
        return data


def get_fibonacci_number(n: int) -> int | str:
    return fibonacci_sequence[n]


def compute_fibonacci_number():
    for i in range(3, config.max_number + 1):
        fibonacci_sequence.append(fibonacci_sequence[-1] + fibonacci_sequence[-2])
