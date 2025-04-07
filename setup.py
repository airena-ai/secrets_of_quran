from setuptools import setup, find_packages

setup(
    name='QuranAnalysis',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'quran_analysis = src.main:main'
        ]
    }
)