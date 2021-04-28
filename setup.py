from setuptools import find_packages, setup

setup(
    name='IndustryIdleEngine',
    packages=find_packages(include=['engine']),
    version='0.1.0',
    description='mock backend of industry idle',
    author='jingming@ualberta.ca',
    license='Apache',
    install_requires=[
        'sqlalchemy',
        'pillow==8.2.0',
        'numpy==1.20.2',
        'pyautogui==0.9.52',
        'opencv-python==4.5.1.48',
        'pywin32',
        'sqlalchemy==1.4.9',
        'BeautifulSoup4==4.9.3',
        'PyQT5==5.15.4',
        'scipy==1.6.2',
        'dbmanager @ https://github.com/History-of-Incomplete-Projects/DBManager/archive/refs/heads/main.zip',
    ]
)
