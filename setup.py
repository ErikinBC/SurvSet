from setuptools import setup
from glob import glob

# ('_datagen', glob('output/**/*', recursive=True)
# data_files = [('readme', 'SurvSet/README.md')]

setup(
    name='SurvSet',
    version='0.1',    
    description='SurvSet package',
    url='https://github.com/ErikinBC/SurvSet',
    author='Erik Drysdale',
    author_email='erikinwest@gmail.com',
    license='BSD 2-clause',
    packages=['SurvSet'],
    package_data={'SurvSet': ['_datagen/output/*','_datagen/figures/*']},
    include_package_data=True,
    install_requires=['numpy', 'pandas'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
    ],
)

