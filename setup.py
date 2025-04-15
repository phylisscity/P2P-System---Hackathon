from setuptools import setup, find_packages

setup(
    name='p2psystem',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'p2psystem = p2psystem.client:main',     # Runs the client
            'startserver = p2psystem.server:main'    # Runs the server
        ]
    },
    author='Phyliss',
    description='Simple peer-to-peer system using sockets',
)
