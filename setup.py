from setuptools import setup

setup(
    name='git-bouncer',
    description='Easy access control for git over ssh',
    license='MIT',
    author='Laurent De Marez',
    author_email='laurent@demarez.org',
    url='https://github.com/lrnt/git-bouncer',
    packages=['bouncer'],
    entry_points={
        'console_scripts': ['git-bouncer = bouncer.cli:main']
    }
)
