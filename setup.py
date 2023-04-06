from setuptools import setup, find_packages

setup(
    name='thread-manager-py',
    version='0.0.3',
    url='https://github.com/sanggi-wjg/py-thread-manager',
    author='SangGi',
    author_email='girr311@naver.com',
    description='Python Thread Manager',
    packages=find_packages(exclude=['tests']),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[],
    zip_safe=False,
    project_urls={
        "Bug Tracker": "https://github.com/sanggi-wjg/py-thread-manager/issues",
    },
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ]
)
