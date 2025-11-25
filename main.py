from cli import CLI, CLIConfig

if "__main__" == __name__:
    cli_config: CLIConfig = CLIConfig(path="./data")
    cli: CLI = CLI(cli_config)

    cli.run()
