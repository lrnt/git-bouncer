from bouncer.cli.base import BaseCommand, noopts, opt


class UserCommand(BaseCommand):
    """ Manage users and their ssh keys """

    _name = 'user'

    @noopts
    def list(self):
        """ List all users """
        pass

    @opt('key', help='Public key file of the user')
    @opt('name', help='Name of the user')
    def add(self, name=None, key=None):
        """ Add a user """
        pass

    @opt('name', help='Name of the user to remove')
    def remove(self):
        """ Remove a user """
        pass
