from setuptools import setup, find_packages

setup(
    name="quran_search_app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pytest"
    ],
    entry_points={
        'console_scripts': [
            'quran_search=src.main:main',
        ],
    },
)