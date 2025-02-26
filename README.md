# Fibonacci API

This project provides a REST API for retrieving Fibonacci numbers. The API is built using FastAPI and includes endpoints for managing a blacklist of numbers.

The unbounded problem is not computable as there is no way to compute the n<sup>th</sup> number without computing all the rest. Thus the current solution bounds the problem to the first 100,000 integers. You may play around with that number but the computation needs grow very fast. The 100,000<sup>th</sup> fibonacci number has 20899 digits. Furthermore in order to save computation resources all the fibonacci numbers are computed once on the server startup and stored in memory. With 100,000 numbers 800KB of memory are requested. Increasing the max number will not only increase the memory requirement but it will also slow down the server start up time.

All these limitations can be removed by off loading the server from the number generation responsibility. A different process can run forever, generate numbers and persist them to disk, ideally to a key value storage. Note that this process can be fault tolerant and in case of failure continue from where it stopped as it only needs to read the last two fibonacci numbers to continue the computation.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Running Tests](#running-tests)
- [License](#license)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/GiorgosPa/fibonacci.git
    cd fibonacci
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:

    ```sh
    uvicorn src.main:app --reload
    ```

2. The API will be available at `http://127.0.0.1:8000`.

## Endpoints

### Fibonacci Endpoints

- **GET /fibonacci/{n}**

    Returns the n-th Fibonacci number.

    **Parameters:**
    - `n`(path): The index of the Fibonacci number to retrieve.
    - `return_type` (query, optional): The return type (`number`, `string`, `auto`). Default is `auto`.

    **Responses:**
    - `200 OK`: Returns the Fibonacci number.
    - `400 Bad Request`: If the number is too large to be returned as a number.
    - `403 Forbidden`: If the number is blacklisted.
    - `422 Unprocessable Entity`: If the input is invalid.

- **GET /fibonacci/**

    Returns a list of Fibonacci numbers.

    **Parameters:**
    - `page` (query, optional): The page number. Default is `1`.
    - `limit` (query, optional): The number of items per page. Default is `100`.

    **Responses:**
    - `200 OK`: Returns a list of Fibonacci numbers.
    - `422 Unprocessable Entity`: If the input is invalid.

### Blacklist Endpoints

- **POST /blacklist/{number}**

    Adds a number to the blacklist.

    **Parameters:**
    - `number` (path): The number to blacklist.

    **Responses:**
    - `200 OK`: If the number is successfully blacklisted.
    - `422 Unprocessable Entity`: If the input is invalid.

- **DELETE /blacklist/{number}**

    Removes a number from the blacklist.

    **Parameters:**
    - `number` (path): The number to whitelist.

    **Responses:**
    - `200 OK`: If the number is successfully whitelisted.
    - `404 Not Found`: If the number is not in the blacklist.
    - `422 Unprocessable Entity`: If the input is invalid.

## Running Tests

To run the tests you need to install the test dependencies as well use the following command:

```sh
pip install '.[tests]'
```

Once done you can run the tests with the following command:

```sh
pytest
```
