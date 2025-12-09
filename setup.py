from setuptools import setup, find_packages

setup(
    name='seleniumUts',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        "undetected-chromedriver>=3.5.5",
        "selenium>=4.15.2"
    ],
    author='Zdek Development team',
    description='Zdek Util libraries for Pythom coding',
    url='https://github.com/SymplaAutomate/selenium-lib',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Zdek Copyright'
    ],
    python_requires='>=3.10',
)
