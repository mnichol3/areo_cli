"""
cli.py

Main command-line interface.
"""
from pathlib import Path
from typing import Optional
from typing_extensions import Annotated

import typer

from aero_cli import __app_name__, __version__, config
from aero_cli.aero_api import AeroAPI


app = typer.Typer()


def _init(
    api_key: Optional[str] = None,
    key_path: Optional[str] = None
) -> str:
    """
    Do stuff.

    Args:
        api_key: str
            FlightAware AeroAPI key.
        key_path: str
            Path of text file containing FlightAware AeroAPI key.

    Returns:
        str
    """
    if api_key is None:
        try:
            api_key = config.init_app(key_path)
        except Exception as err:
            print(err)
            typer.Exit(1)

    #os.environ['AEROAPI_KEY'] = api_key
    return api_key


@app.command()
def init(
    api_key: Annotated[
        str,
        typer.Option(
            "--api-key",
            "-k",
            help="FlightAware AeroAPI key."
        )
    ] = None,
    key_path: Annotated[
        str,
        typer.Option(
            "--key-file",
            "-f",
            help="Path of file containing FlightAware AeroAPI key."
        )
    ] = None,
) -> None:
    """
    Initialize an AeroAPI instance.

    Args:
        api_key: str, optional
        key_path : str, optional

    Returns:
        None
    """
    _init(api_key=api_key, key_path=key_path)
    # TODO: add file output?


@app.command()
def arrivals(
    airport: Annotated[
        str,
        typer.Argument(
            help="Airport 4-letter ICAO code, e.g. 'KLAX'."
        )
    ],
    carrier: Annotated[
        str,
        typer.Option(
            "--carrier",
            "-c",
            help="Carrier/airline operating the route."
        )
    ] = None,
) -> None:
    """
    Get the arrivals for an airport.

    Args:
        airport: str
            4-letter ICAO code, e.g. 'KLAX'.
        carrier: str, optional
            3-letter airline/carrier code, e.g. 'UAL'.

    Returns:
        None
    """
    api_key = _init()
    api = AeroAPI(api_key=api_key)
    result, _ = api.get_arrivals(airport, carrier=carrier)


@app.command()
def sched_arrivals(
    airport: Annotated[
        str,
        typer.Argument(
            help="Airport 4-letter ICAO code, e.g. 'KLAX'."
        )
    ],
    carrier: Annotated[
        str,
        typer.Option(
            "--carrier",
            "-c",
            help="Carrier/airline operating the route."
        )
    ] = None,
) -> None:
    """
    Get the scheduled arrivals for an airport.

    Args:
        airport: str
            4-letter ICAO code, e.g. 'KLAX'.
        carrier: str, optional
            3-letter airline/carrier code, e.g. 'UAL'.

    Returns:
        None
    """
    api_key = _init()
    api = AeroAPI(api_key=api_key)
    result, _ = api.get_scheduled_arrivals(airport, carrier=carrier)


@app.command()
def departures(
    airport: Annotated[
        str,
        typer.Argument(
            help="Airport 4-letter ICAO code, e.g. 'KLAX'."
        )
    ],
    carrier: Annotated[
        str,
        typer.Option(
            "--carrier",
            "-c",
            help="Carrier/airline operating the route."
        )
    ] = None,
) -> None:
    """
    Get the departures for an airport.

    Args:
        airport: str
            4-letter ICAO code, e.g. 'KLAX'.
        carrier: str, optional
            3-letter airline/carrier code, e.g. 'UAL'.

    Returns:
        None
    """
    api_key = _init()
    api = AeroAPI(api_key=api_key)
    result, _ = api.get_departures(airport, carrier=carrier)


@app.command()
def sched_departures(
    airport: Annotated[
        str,
        typer.Argument(
            help="Airport 4-letter ICAO code, e.g. 'KLAX'."
        )
    ],
    carrier: Annotated[
        str,
        typer.Option(
            "--carrier",
            "-c",
            help="Carrier/airline operating the route."
        )
    ] = None,
) -> None:
    """
    Get the scheduled departures for an airport.

    Args:
        airport: str
            4-letter ICAO code, e.g. 'KLAX'.
        carrier: str, optional
            3-letter airline/carrier code, e.g. 'UAL'.

    Returns:
        None
    """
    api_key = _init()
    api = AeroAPI(api_key=api_key)
    result, _ = api.get_scheduled_departures(airport, carrier=carrier)


@app.command()
def flights_between(
    origin: Annotated[
        str,
        typer.Argument(
            help="Origin airport 4-letter ICAO code, e.g. 'KLAX'."
        )
    ],
    dest: Annotated[
        str,
        typer.Argument(
            help="Destination airport 4-letter ICAO code, e.g. 'KLAX'."
        )
    ],
    carrier: Annotated[
        str,
        typer.Option(
            "--carrier",
            "-c",
            help="Carrier/airline operating the route."
        )
    ] = None,
) -> None:
    """
    Get flights between an origin and destination airport.

    Args:
        origin: str
            4-letter ICAO code of the origin airport, e.g. 'KLAX'.
        dest: str
            4-letter ICAO code of the destination airport, e.g. 'KLAX'.
        carrier: str, optional
            3-letter airline/carrier code, e.g. 'UAL'.

    Returns:
        None
    """
    api_key = _init()
    api = AeroAPI(api_key=api_key)
    result, _ = api.get_flights_between(origin, dest, carrier=carrier)


@app.command()
def route(
    ident: Annotated[
        str,
        typer.Argument(
            help="The fa_flight_id to fetch."
        )
    ],
    outfile: Annotated[
        Path,
        typer.Option(
            "-o",
            "--out",
            help="Path of output file."
        )
    ] = None
) -> None:
    """
    Get information about a flight's filed route including coordinates, names,
    and types of fixes.

    Args:
        ident: str
            FlightAware fa_flight_id to fetch.
        outfile: str, optional
            Path of the file to write output to.

    Returns:
        None.
    """
    raise NotImplementedError


@app.command()
def track(
    ident: Annotated[
        str,
        typer.Argument(
            help="The fa_flight_id to fetch."
        )
    ],
    outfile: Annotated[
        Path,
        typer.Option(
            "-o",
            "--out",
            help="Path of output file."
        )
    ] = None
) -> None:
    """
    Get the track for a flight as a series of positions.

    Args:
        ident: str
            FlightAware fa_flight_id to fetch.
        outfile: str, optional
            Path of the file to write output to.

    Returns:
        None.
    """
    raise NotImplementedError


def _version_callback(value: bool) -> None:
    """
    Print app name & version.

    Args:
        value: bool

    Returns:
        None
    """
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
