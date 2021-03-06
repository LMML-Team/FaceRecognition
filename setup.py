from distutils.core import setup
from setuptools import find_packages

try:
    import camera
except ImportError:
    print("Warning: `camera` must be installed in order to use `face_recognition`")

try:
    import dlib_models
except ImportError:
    print("Warning: `dlib_models` must be installed in order to use `face_recognition`")

try:
    import skimage.io
except ImportError:
    print("Warning: `skimage.io` must be installed in order to use `face_recognition`")


setup(name='face_recognition',
      version='1.0',
      description='Identifies faces',
      authors='Michael Lai (@impostercafe), Amanda Wang (@CandyMandy28), Anthony Cavallaro (@QuantatativeFinancier), Petar Griggs (@Anonymission)',
      author_email="mlai8088@gmail.com",
      packages=find_packages(),
      license="MIT"
      )
