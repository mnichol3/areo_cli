"""
config.py

Find the AeroAPI key from various sources.
"""
import os
from typing import Optional

import typer

from aero_cli.exceptions import APIKeyError


def init_app(key_path: Optional[str] = None) -> str:
    """
    Check for the existence of the AeroAPI key as en environment variable or
    in a text file.

    Args:
        key_path: str, optional
            Path of the text file containing the FlightAware AeroAPI key.
            If not given, then the 'AEROAPI_KEY' environment variable must be set.

    Returns:
        str: AeroAPI key

    Raises:
    """
    try:
        api_key = os.environ['AEROAPI_KEY']
    except KeyError:
        if key_path is not None:
            try:
                api_key = _get_key_from_file(key_path)
            except FileNotFoundError:
                msg = f'AeroAPI key not found in "AEROAPI_KEY" env var or file {key_path}.'
                raise APIKeyError(msg)
        else:
            raise APIKeyError('AeroAPI key not found in "AEROAPI_KEY" env var.')

    return api_key


def _get_key_from_file(key_path: str) -> str:
    """
    Read FlightAware AeroAPI key from a file.

    Args:
        key_path: str
            Path of key file.

    Returns: str
        Key value.

    Raises:
        FileNotFoundError
    """
    with open(key_path, 'r') as key_file:
        key = key_file.read().rstrip()

    return key
