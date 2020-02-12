"""
Package setup.

This file is used to package the whole project.
"""

import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='WHU-ScoreChecker',
    version='1.0.1',
    author='Tony Xiang',
    author_email='tonyxfy@qq.com',
    description='A simple, open-source and model-driven score checker for \
WHU.',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/T0nyX1ang/WHU-ScoreChecker',
    packages=setuptools.find_packages(include=['scorechecker',
                                               'scorechecker.*']),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.5, <3.8',
    entry_points={
        'console_scripts': [
            'scorechecker=scorechecker.main:run',
        ],
    },
    install_requires=[
        'Keras>=2.3.1',
        'lxml>=4.3.2',
        'opencv_python>=4.1.0.25',
        'keyring>=20.0.1',
        'requests>=2.21.0',
        'numpy>=1.16.2',
        'pycryptodome>=3.9.6',
        'beautifulsoup4>=4.7.1',
        'tensorflow==2.0.1'
    ]
)
