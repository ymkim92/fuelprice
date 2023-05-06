from setuptools import find_packages, setup

setup(
    name="fuel_price",
    scripts=["bin/racq_fuel_price"],
    version="0.2",
    description="Fuel price in Queensland, Australia",
    author="Youngmin Kim",
    author_email="ymkim92@gmail.com",
    license="WTFPL",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "requests",
    ],
)
