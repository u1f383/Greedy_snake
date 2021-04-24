# Reference: https://github.com/pypa/sampleproject

# setuptools >> distutils
from setuptools import setup, find_packages
import pathlib

# get current absolute path
curr_path = pathlib.Path(__file__).parent.resolve()
long_description = (curr_path / 'README.md').read_text(encoding='utf-8')

# pip install greedySnake
setup(
    name="greedySnake",
    version='1.0.0',
    description='greedy snake game in python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/u1f383/Greedy_snake',
    author='u1f383',
    author_email='cc85nod@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.8'
    ],
    keywords='greedy, snake',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.8',
    install_requires=[
        'pygame==2.0.1'
    ],
    project_urls={
        'Source': 'https://github.com/u1f383/Greedy_snake',
    },
)