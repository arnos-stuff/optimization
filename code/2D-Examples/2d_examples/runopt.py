import typer
import rich
import numpy as np

from .inputs import pipeInput, console

app = typer.Typer(
    help="""Perform optimization related tasks.  
    
    First, basic tasks:
    \t - [bold green]runopt[/bold green] [bold yellow]grideval[/bold yellow] helps you evaluate a function and it's derivatives on a grid.
    \t - [bold green]runopt[/bold green] [bold yellow]slice[/bold yellow] helps you slice a grid along a ray or a line / slab.
    \t - [bold green]runopt[/bold green] [bold yellow]plot[/bold yellow] helps you plot a function along a ray or a line / slab.
    
    
    👉 the typical workflow is:
    \t 1. [bold green]runopt[/bold green] [bold yellow]def[/bold yellow] --func [bold blue]func[/bold blue] --grid [bold blue]grid[/bold blue] --expr [bold blue]<function>[/bold blue] to define your function (or give it as a file).
    \t 2. [bold green]runopt[/bold green] [bold yellow]grideval[/bold yellow] --func [bold blue]func[/bold blue] --grid [bold blue]grid[/bold blue] --out [bold blue]out[/bold blue] to get a CSV file with the function values.
    \t 3. [bold green]runopt[/bold green] [bold yellow]slice[/bold yellow] --grid [bold blue]grid[/bold blue] --csv [bold blue]out[/bold blue] --out [bold blue]out[/bold blue] to get a CSV file with the function values along a ray if you want to plot it.
    \t 4. [bold green]runopt[/bold green] [bold yellow]plot[/bold yellow] --csv [bold blue]out[/bold blue] --out [bold blue]out[/bold blue] to plot the function values contained in the CSV file.
    """
    name="runopt",
    add_completion=True,
    no_args_is_help=True,
    help_option_names=["-h", "--help"],
)

grideval = typer.Typer(
    "grideval",
    "Evaluate a function and it's derivatives on a grid.",
    add_completion=True,
    no_args_is_help=True,
    help_option_names=["-h", "--help"],
)

@grideval.command(""