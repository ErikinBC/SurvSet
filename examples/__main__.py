"""
Contains the code found in the README. Designed to ensure it compiles properly.

# To run:
>>> python3 -m examples
"""

def main() -> None:
    # Examples
    from . import example_simple, example_complex

    print('Checking simple example...')
    example_simple()
    print('Example #1 complete!')

    print('Checking complex example...')
    example_complex()
    print('Example #2 complete!')
    


if __name__ == "__main__":
    main()
    