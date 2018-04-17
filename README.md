# tensorflow serving 실행법
## tensorflow-serving-api 설치
서버단

Installation

https://www.tensorflow.org/serving/setup

serving용 모델 생성
python deploy/export_model.py [case] [path]

예시
python deploy/export_model.py voxceleb_large_4s /data/private/voice-vector/saved_model/

tensorflow serving 실행
nohup tensorflow_model_server --port=1027 --model_name=voice_vector --model_base_path=/data/private/voice-vector/saved_model/ &

클라이언트

pip install tensorflow-serving-api
