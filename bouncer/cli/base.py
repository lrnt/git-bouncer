import configparser
import sys
import inspect

from argparse import ArgumentParser, RawDescriptionHelpFormatter


def opt(*args, **kwargs):
    def decorator(method):
        if not hasattr(method, 'options'):
            method.options = []
        method.options.append((args, kwargs))
        return method
    return decorator


def noopts(method):
    method.options = []
    return method


class HelpMixin(object):
    def help(self):
        print('available commands:')
        for name, command in self.commands.items():
            description = str(command.__doc__ or '').strip('\n')
            print('  ', name.ljust(10), description)
        return 1


class SubParser(HelpMixin):
    def __init__(self, commands):
        self.commands = self._commands(commands)

    def _commands(self, commands):
        prog = sys.argv[0]
        result = {}
        for cmd in commands:
            name = getattr(cmd, '_name', None)
            if not name:
                continue
            cmd.prog = prog
            result[name] = cmd
        return result

    def run(self):
        args = sys.argv[1:]
        for index, arg in enumerate(args):
            if arg in self.commands.keys():
                args.pop(index)
                return self.commands[arg](args)
        return self.help()


class Command(HelpMixin):
    def __init__(self):
        self.global_options = []
        self.commands = self._methods_with_opts()

    def _methods_with_opts(self):
        result = {}
        for name in dir(self):
            if name.startswith('__'):
                continue
            method = getattr(self, name)
            if not hasattr(method, 'options'):
                continue
            result[name] = method
        return result

    def _parse_args(self, method, args):
        prog = '{} {} {}'.format(self.prog, self._name, method.__name__)
        parser = ArgumentParser(
            prog=prog,
            description=(method.__doc__ or ''),
            formatter_class=RawDescriptionHelpFormatter
        )

        for opt in method.options + self.global_options:
            parser.add_argument(*opt[0], **opt[1])

        return vars(parser.parse_args(args))

    def _call_method(self, method, args):
        # Find out which arguments the method expects
        expected_args, _, _, _ = inspect.getargspec(method)
        expected_args.remove('self')

        self_args = self._parse_args(method, args)
        method_args = {}

        # Get the expected method arguments, ignore rest
        for name in expected_args:
            if name in args:
                method_args[name] = args.pop(name)

        # Put rest of the arguments in self
        for name, value in self_args.items():
            setattr(self, name, value)

        self.pre_command()

        return method(**method_args)

    def __call__(self, args):
        for index, arg in enumerate(args):
            if arg in self.commands.keys():
                args.pop(index)
                return self._call_method(self.commands[arg], args)
        return self.help()

    def opt(self, *args, **kwargs):
        self.global_options.append((args, kwargs))

    def pre_command(self):
        pass


class BaseCommand(Command):
    def __init__(self):
        super(BaseCommand, self).__init__()
        self.opt(
            '-c', dest='config_path', help='Configuration file',
            default='~/.test.conf'
        )

    def pre_command(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)
        print(config.sections())
