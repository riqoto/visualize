from cli import CLI, CLIConfig

if "__main__" == __name__:
    cli_config: CLIConfig = CLIConfig(path="/home/bhh/Belgeler/visiual/visualize/data")
    cli: CLI = CLI(cli_config)
    cli.run()
