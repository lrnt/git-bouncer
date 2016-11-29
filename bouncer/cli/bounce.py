from bouncer.cli.base import BaseCommand, noopts


class BounceCommand(BaseCommand):
    """ Bounce incomming git communication through ssh """

    _name = 'bounce'

    @noopts
    def run(self):
        """ Run the bouncer """
        pass

    @noopts
    def rebuild(self):
        """ Rebuild the authorized_keys file """
        pass
