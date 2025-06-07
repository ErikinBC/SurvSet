"""
Calls all the relevant modules. These should execute locally before any package updates are pushed.

# To run:
>>> python3 -m tests
"""

def main():
    # Relevant modules
    from SurvSet.__main__ import main as survset_main
    from SurvSet.data import _surv_test
    from examples.__main__ import main as example_main
    from SurvSet._datagen.__main__ import main as datagen_main
    from simulation.__main__ import main as simulation_main

    # SurvSet main module
    survset_main()
    print('SurvSet.__main__ complete!')
    
    # Test the SurvLoader class
    _surv_test()
    print('SurvSet.data test complete!')
    
    # README examples
    example_main()
    print('Examples.__main__ complete!')

    # Data
    datagen_main()
    print('SurvSet._datagen complete!')
    
    # Simulation
    simulation_main()
    print('Simulation.__main__ complete!')


if __name__ == "__main__":
    # Call the main module
    main()