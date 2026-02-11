from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]

setup(
    name="seleniumUts",
    version="1.1.6",
    packages=find_packages(),
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    install_requires=["undetected-chromedriver>=3.5.5", "selenium>=4.15.2"],
    author="Zdek Development team",
    description="Zdek Util libraries for Pythom coding",
    url="https://github.com/ZdekPyPi/SeleniumUts",
    license="MIT",
    keywords="seleniumUts",
    classifiers=classifiers,
    python_requires=">=3.10",
)
