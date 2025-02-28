from setuptools import setup, find_packages

setup(
    name='VulnScanner',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pytest',
    ],
    entry_points={
        'console_scripts': [
            'vulnscanner=scripts.vuln_scanner:main',
        ],
    },
)
