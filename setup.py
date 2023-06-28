from setuptools import setup, find_namespace_packages

setup(
    name='bot-personal-assistant',
    version='0.1.3',
    description='Console bot helps manage contacts, notes and sort file',
    author='Andrii Chychur',
    author_email='a.chy-test@gmail.com',
    url='https://github.com/chychur/m02_01',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'],
    packages=find_namespace_packages(),
    include_package_data=True,
    entry_points={'console_scripts': [
        'startbot=BotAssistant.bot:run']
    }
)
