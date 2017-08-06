# FaceRecognition
This is a student group project for MIT Beaver Works Summer Institute 2017: Cognitive Assistant Collaboration.

The project is designed to detect a face and, with user input, save photos to a database of facial descriptors. This project can also categorize unlabeled, unsorted photos from a given directory

# Setup
Install these packages and follow the instructions as stated: [Camera](https://github.com/LLCogWorks2017/Camera)
[Dlib Models](https://github.com/LLCogWorks2017/DlibModels)
[Scikit Image](http://scikit-image.org/docs/dev/install.html)

Clone this repository.
Open the folder of the cloned repository in Command Prompt.
Enter this command:
```shell
python setup.py develop
```

# Database
To import this package, there must be at least one face descriptor in the database (stored in face_data.pickle). The face_data.pickle file that comes with this package has a number of faces already stored; however if you wish to use your own photos and delete the face_data.pickle file instead of using the clear_database function (as is the preferred method), to avoid any errors upon importing, comment out the following lines from the top of config.py:
```shell
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "face_data.pickle"), 'rb') as f:
    face_data = pickle.load(f)
```
