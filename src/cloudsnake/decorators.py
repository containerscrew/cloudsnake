import functools

import typer
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError

from cloudsnake.console import console


def handle_aws_errors(func):
    """
    Decorator to handle common AWS (boto3) exceptions gracefully
    and print error messages to the CLI.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except NoCredentialsError:
            console.print(
                "[bold red]Credentials Error:[/bold red] Unable to locate AWS credentials. "
                "Please run [bold]aws configure[/bold] or check your environment variables."
            )
            raise typer.Exit(1)

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_msg = e.response["Error"]["Message"]
            console.print(f"[bold red]AWS Error ({error_code}):[/bold red] {error_msg}")
            raise typer.Exit(1)

        except BotoCoreError as e:
            console.print(f"[bold red]AWS Configuration Error:[/bold red] {str(e)}")
            raise typer.Exit(1)

        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled by user.[/yellow]")
            raise typer.Exit(0)

    return wrapper
