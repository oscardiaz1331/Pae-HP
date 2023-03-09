from setuptools import find_packages, setup

setup(
    name='hpverif',
    packages=find_packages(include=['hpverif']),
    version='0.1.3',
    install_requires = [
    'pyrealsense2',
    'numpy',
    'opencv-python',
    'matplotlib'
    ],
    description='Hp construction verification library PAE 2023',
    author='Alejandro Amat',
    license='MIT',
)