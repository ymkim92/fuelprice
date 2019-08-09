from setuptools import setup, find_packages

setup(name='fuel_price',
    scripts=['bin/racq_fuel_price'],
    version='0.1',
    description='Fuel price in Queensland, Australia',
    author='Youngmin Kim',
    author_email='ymkim92@gmail.com',
    license='WTFPL',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'requests',
    ],
)