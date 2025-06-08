from setuptools import setup, find_packages
from setuptools.command.install import install
import os

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # Add any post-installation steps here

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('config')
extra_files.extend(package_files('data'))
extra_files.extend(package_files('models'))
extra_files.extend(package_files('outputs'))

setup(
    name='FraudDetector',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/yourusername/FraudDetector',
    license='MIT',
    author='Your Name',
    author_email='your.email@example.com',
    description='Credit Card Fraud Detection System',
    install_requires=[
        'numpy>=1.21.0',
        'pandas>=1.5.0',
        'scikit-learn>=1.0.0',
        'imbalanced-learn>=0.8.0',
        'joblib>=1.0.0',
        'matplotlib>=3.4.0',
        'seaborn>=0.11.0',
        'xgboost>=1.5.0'
    ],
    package_data={'': extra_files},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'fraud_detector=main:main',
            'fraud_detector_gui=gui.fraud_detector_gui:main'
        ]
    },
    cmdclass={
        'install': PostInstallCommand,
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
