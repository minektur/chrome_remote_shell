import chrome_remote_shell
import sys
from distutils.core import setup

requirements = []

setup(
    name='chrome_remote_shell',
    version='1.2',
    description='Client for talking to the Google Chrome remote shell port',
    long_description=chrome_remote_shell.__doc__.split('\n\n', 1)[1],
    author='Fred Clift and Brandon Craig Rhodes',
    author_email='fred@clift.org',
    url='https://github.com/minektur/chrome_remote_shell',
    packages=['chrome_remote_shell'],
    platforms='any',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        ],
    install_requires=['websocket-client'],
    )
