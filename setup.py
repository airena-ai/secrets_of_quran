from setuptools import setup, find_packages

setup(
    name='quran_text_analysis',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'quran_text_analysis = src.main:main'
        ]
    }
)