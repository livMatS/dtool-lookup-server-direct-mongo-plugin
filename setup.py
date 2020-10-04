from setuptools import setup

url = "https://github.com/IMTEK-Simulation/dtool-lookup-server-direct-mongo-plugin"
version = "0.1.0"
readme = open('README.rst').read()

setup(
    name="dtool-lookup-server-direct-mongo-plugin",
    packages=["dtool_lookup_server_direct_mongo_plugin"],
    description="""This plugin allows to submit mongo queries and aggregation
                   pipelines directly to the lookup server's underlying MongoDB.""",
    long_description=readme,
    author="Johannes Hörmann",
    author_email="johannes.hoermann@imtek.uni-freiburg.de",
    version=version,
    url=url,
    entry_points={
        'dtool_lookup_server.blueprints': [
            'dtool_lookup_server_direct_mongo_plugin=dtool_lookup_server_direct_mongo_plugin:mongo_bp',
        ],
    },
    install_requires=[
        "dtool-lookup-server",
    ],
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
