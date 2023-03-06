from setuptools import find_packages, setup

setup(
    name='realsenseverif',
    packages=find_packages(include=['realsenseverif']),
    version='0.1.2',
    install_requires = [
    'pyrealsense2',
    'numpy',
    'opencv-python',
    'matplotlib'
    ],
    description='Hp verification library PAE 2023',
    author='Alejandro Amat',
    license='MIT',
)