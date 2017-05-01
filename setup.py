from setuptools import setup


setup(
    name='soundcollide',
    packages=['soundcollide'],
    include_package_data=True,
    install_requires=[
        'flask',
        'mysql-connector==2.1.4'
    ],
)
