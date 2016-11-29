from bouncer.cli.base import SubParser
from bouncer.cli.bounce import BounceCommand
from bouncer.cli.user import UserCommand
from bouncer.cli.repo import RepoCommand


def main():
    SubParser([
        BounceCommand(),
        UserCommand(),
        RepoCommand()
    ]).run()


if __name__ == '__main__':
    main()
