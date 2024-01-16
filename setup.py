from setuptools import setup,find_namespace_packages

setup(name='personal-assistant',
      version='1.0',
      description='This project is created to develop a command-line interface personal assistant for contact management, note-taking, and file sorting.',
      url='https://nyambevos.github.io/Personal-assistant/',
      author='Daiquiri Club',
      author_email='daiquiri_club@team.com',
      license='MIT',
      packages=find_namespace_packages(),
      entry_points = {'console_scripts': ['assistantdc=personal_assistant.main:main'],},
      install_requires=['colored==2.2.4', 'prompt-toolkit==3.0.43', 'wcwidth==0.2.13'],
      )