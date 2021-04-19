import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(
    name='pycci',
    packages=find_packages(include=['pycci']),
    include_package_data=True,
    version='1.0.0',
    description='CircleCI API written in python',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/winslowdibona/pycci',
    author='Winslow DiBona',
    license='MIT',
    install_requires=['pyyaml', 'requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)
