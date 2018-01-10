from setuptools import setup, find_packages

setup(
    name='BibFast',
    version='0.1',
    packages=find_packages(exclude=['test']),
    url='https://github.com/Shvarpa/BibFast',
    license='',
    author='Shvarpa',
    author_email='Shvarpa@gmail.com',
    description='citation firebase database',
    install_requires=['requests==2.11.1',
                      'gcloud==0.17.0',
                      'oauth2client==3.0.0',
                      'requests_toolbelt==0.7.0',
                      'python_jwt==2.0.1',
                      'pycryptodome==3.4.3'
					  'pyrebase'
                      ],
    entry_points='''
    [console_scripts]
    bib=BibFast:cli
    ''',

)
