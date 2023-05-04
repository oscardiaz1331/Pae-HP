from setuptools import find_packages, setup

setup(
    name='hpverif',
    packages=find_packages(include=['hpverif']),
    version='1.6.3',
    install_requires = [
    'pyrealsense2',
    'numpy',
    'opencv-python',
    'matplotlib',
    'scipy',
    'sklearn',
    'open3d',
    'imageio',
    'ast'
    ],
    description='Construction verification library PAE 2023',
    author='Telecos PAE 2023 Students',
    license='MIT',
)