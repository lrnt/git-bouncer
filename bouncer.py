#!/usr/bin/env python

import os
import re
import sys

VERB_READ = ['upload-pack', 'upload-archive']
VERB_WRITE = ['receive-pack']
VERB_ALL = set(VERB_READ + VERB_WRITE)

RE_CMD_PATH = re.compile(
    r"^git[- ](?P<verb>({})) '/*(?P<path>.*)'$".format('|'.join(VERB_ALL))
)

CONFIG = {
    'example.git': {
        'destination': '/home/git/example',
        'all': ['laurent']
    }
}


class GitError(Exception):
    pass


class GitCommand(object):
    def __init__(self, config, cmd):
        match = RE_CMD_PATH.match(cmd)

        if not match:
            raise GitError('Git protocol error')

        self.verb = match.group('verb')
        self.path = match.group('path')
        self.config = {
            'all': [],
            'read': [],
            'write': []
        }

        try:
            self.config.update(config[self.path])
            self.destination = self.config['destination']
        except KeyError:
            raise GitError('Could not find repository')

    @property
    def action(self):
        return 'write' if self.verb in VERB_WRITE else 'read'

    @property
    def cmd(self):
        return "git {} '{}'".format(self.verb, self.destination)

    def has_permissions(self, user):
        return user in set(self.config['all'] + self.config[self.action])

    def execute(self, user):
        if not self.has_permissions(user):
            raise GitError('Insufficient permissions to continue')
        os.execvp('git', ['git', 'shell', '-c', self.cmd])


if __name__ == '__main__':
    user = sys.argv[1]
    ssh_command = os.environ.get('SSH_ORIGINAL_COMMAND', '')

    try:
        git_command = GitCommand(CONFIG, ssh_command)
        git_command.execute(user)
    except GitError as e:
        sys.exit("ERROR: {}".format(e))
