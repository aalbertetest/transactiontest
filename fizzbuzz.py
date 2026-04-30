def print_fizzbuzz() -> None:
    """Print 1–100; Fizz for multiples of 3, Buzz for 5, FizzBuzz for both."""
    for n in range(1, 101):
        if n % 15 == 0:
            print("FizzBuzz")
        elif n % 3 == 0:
            print("Fizz")
        elif n % 5 == 0:
            print("Buzz")
        else:
            print(n)


if __name__ == "__main__":
    print_fizzbuzz()
