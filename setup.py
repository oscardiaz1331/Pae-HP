from setuptools import find_packages, setup

setup(
    name='hpverif',
    packages=find_packages(include=['hpverif']),
    version='2.5.4',
    install_requires = [
    'pyrealsense2',
    'numpy',
    'opencv-python',
    'matplotlib',
    'scipy',
    'open3d',
    'imageio'
    ],
    description='Construction verification library PAE 2023',
    author='Telecos PAE 2023 Students',
    license='MIT',
)