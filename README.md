# Voice Vector Web
## How to set up?
### Server Side (Tensorflow serving)
python 2.7

#### Installation
https://www.tensorflow.org/serving/setup

#### Export model
* `python deploy/export_model.py [case] [path]`
  * Ex) `python deploy/export_model.py voxceleb_large_4s /data/private/voice-vector/saved_model/`

#### Run tensorflow model server
`nohup tensorflow_model_server --port=1027 --model_name=voice_vector --model_base_path=/data/private/voice-vector/saved_model/ &`

### Client Side (Flask)
python 3.5

### Install
#### ffmpeg
`sudo apt-get install ffmpeg`
#### tensorflow serving api
`pip install tensorflow-serving-api-python3`

#### https settings
refer to https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https

### Run server
python run.py