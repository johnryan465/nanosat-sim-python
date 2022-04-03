import setuptools

extras = {
    "orekit": [],
    "poliastro": []
}

setuptools.setup(
    name='nanosatsim',
    packages=['nanosatsim'],
    package_dir={'': 'src'},
    version="0.0.1",
    author="John Ryan",
    author_email="john.patrick.ryan.ie@gmail.com",
    description="A small example package",
    url="https://github.com/gituser/example-pkg",
    license='GPT',
    extras_require=extras,
    python_requires='>=3.9',
    install_requires=[]
)
