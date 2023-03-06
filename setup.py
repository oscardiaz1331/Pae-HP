from setuptools import find_packages, setup

setup(
    name='realsenseverif',
    packages=find_packages(),
    version='0.1.0',
    install_requires = [
    'pyrealsense2',
    'numpy',
    'opencv-python',
    'matplotlib',
    'tensorflow'
    ],
    description='Hp verification library PAE 2023',
    author='PAE-HP',
    license='MIT',
)