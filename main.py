import logging
from prompt_toolkit import PromptSession
from utils.constants import (
    WELCOME_MESSAGE, HELP_PROMPT, GOODBYE_MESSAGE, USE_EXIT_MESSAGE, invalid_command_message_tooltip
)
from cli.cli import GraphDBLiteCLI

def process_command(cli: GraphDBLiteCLI, command: str) -> bool:
    if not command.strip():
        return True
    cmd, args = cli.parse_command(command)
    handler = cli.command_map.get(cmd)
    if handler:
        try:
            return handler(args)
        except Exception as e:
            cli.print_error(f"Unexpected error: {str(e)}")
            logging.error(f"Error processing command '{command}': {e}")
            return False
    else:
        cli.print_error(f"Unknown command: {cmd}")
        cli.print_info(invalid_command_message_tooltip)
        return False

def run(cli: GraphDBLiteCLI):
    session = PromptSession(
        completer=cli.completer,
        style=cli.style
    )
    print(WELCOME_MESSAGE)
    print(HELP_PROMPT)
    print()
    while not cli.should_exit:
        try:
            command = session.prompt('GraphDBLite> ')
            if not process_command(cli, command):
                break
        except KeyboardInterrupt:
            print(f"\n{USE_EXIT_MESSAGE}")
        except EOFError:
            break
        except Exception as e:
            cli.print_error(f"Unexpected error: {str(e)}")
            logging.error(f"Unexpected error in main loop: {e}")
    print(GOODBYE_MESSAGE)

def main():
    cli = GraphDBLiteCLI()
    run(cli)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        filename='app.log',
        filemode='a'
    )
    main()