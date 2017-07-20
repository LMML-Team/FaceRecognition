from setuptools import setup, find_packages


def do_setup():
    setup(name='camera',
          version="0.0",
          author='Ryan Soklaski',
          description='Simple API for configuring.using camera in Python',
          license='MIT',
          platforms=['Windows', 'Linux', 'Mac OS-X', 'Unix'],
          packages=find_packages())

if __name__ == "__main__":
    do_setup()
