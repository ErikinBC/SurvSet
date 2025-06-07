"""
Contains utility functions
"""

# External imports
import argparse


def get_args(
        di_argparse_defaults: dict,
        description: str | None = None,
        ) -> argparse.Namespace:
    """
    Convenience wrapper for passing in argparse defaults in the form of a dictionary that looks like:
    {
        'arg_name': {'val': default_value, 'type': type, 'help': help_text},
        ...
    }
    """
    # Input checks
    assert isinstance(di_argparse_defaults, dict), 'di_argparse_defaults must be a dictionary'
    assert description is None or isinstance(description, str), 'description must be a string or None'
    # Loop through the dictionary and add arguments to the parser
    parser = argparse.ArgumentParser(description=description)
    for arg_name, arg_info in di_argparse_defaults.items():
        assert isinstance(arg_name, str), 'arg_name must be a string'
        assert isinstance(arg_info, dict), 'arg_info must be a dictionary'
        assert 'val' in arg_info, 'arg_info must contain a "val" key'
        assert 'type' in arg_info, 'arg_info must contain a "type" key'
        assert 'help' in arg_info, 'arg_info must contain a "help" key'
        parser.add_argument(f'--{arg_name}', default=arg_info['val'], type=arg_info['type'], help=arg_info['help'])
    # Parse the arguments
    args = parser.parse_args()
    return args
