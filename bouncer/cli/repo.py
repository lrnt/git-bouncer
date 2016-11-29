from bouncer.cli.base import BaseCommand, noopts, opt


class RepoCommand(BaseCommand):
    """ Manage git repositories and their access rules """

    _name = 'repo'

    @noopts
    def list(self):
        """ List all repositories """
        pass

    @opt('path', help='Local path to the repository')
    @opt('name', help='Public name of the repository')
    @opt('--all', '-a', help='People who have read/write permissions')
    @opt('--write', '-w', help='People who have write permissions')
    @opt('--read', '-r', help='People who have read permissions')
    def add(self):
        """ Add a repository """
        pass

    @opt('name', help='Public name of the repository')
    def remove(self):
        """ Remove a repository """
        pass

    @opt('name', help='Public name of the repository')
    @opt('--all', '-a', help='People who have read/write permissions')
    @opt('--write', '-w', help='People who have write permissions')
    @opt('--read', '-r', help='People who have read permissions')
    def edit(self):
        """ Edit a repository """
        pass
