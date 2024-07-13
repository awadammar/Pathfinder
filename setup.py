from setuptools import setup, find_packages

setup(
    name='pathfinder',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
         'shapely',
            'matplotlib',
            'networkx',
            'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'pathfinder=src.pathfinder.main:main',
        ],
    },
    description='A CLI tool to find the shortest path avoiding obstacles.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
