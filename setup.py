from setuptools import setup, find_packages

setup(
    name="quick_fetch",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # List any dependencies your project has here
    ],
    entry_points={
        'console_scripts': [
            'quick_fetch = quick_fetch.main:run',
        ],
    },
)