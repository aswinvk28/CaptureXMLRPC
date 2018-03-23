from setuptools import setup

setup(
    name='CaptureXMLRPC',
    packages=['CaptureXMLRPC'],
    include_package_data=True,
    install_requires=[
        'flask', 'Flask-XML-RPC'
    ],
)