from setuptools import setup


REQUIREMENTS = {
    'base': [
            'confluent_kafka==1.4.2',
            'requests==2.24.0',
            'psycopg2==2.8.6'
            ],
    'test': []
}
setup(
    name='kwebsitemonitoring',
    version='0.0.1',
    package_dir={'': 'src'},
    packages=['kwebsitemonitoring'],
    url='https://github.com/krzysbaranski/kwebsitemonitoring',
    license='GNU Affero General Public License Version 3',
    author='Krzysztof Baranski',
    author_email='baranski5@gmail.com',
    description='HTTP Website Status monitoring',
    install_requires=REQUIREMENTS['base'],
    tests_require=REQUIREMENTS['test']
)
