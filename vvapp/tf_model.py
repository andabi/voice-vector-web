from __future__ import print_function

import sys

sys.path.append('.')
sys.path.append('..')

from grpc.beta import implementations
import tensorflow as tf

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2

from vvapp.audio import wav2melspec_db, normalize_db, fix_length, read_wav_from_stream
import numpy as np

from vvapp import app
host = app.config['TF_SERVER_HOST']
port = app.config['TF_SERVER_PORT']

duration, sr, n_fft, win_length, hop_length, n_mels, max_db, min_db = 4, 16000, 512, 512, 128, 80, 35, -55


def request_sim(stream):
    wav = read_wav_from_stream(stream, sr)
    wav = fix_length(wav, sr * duration, mode='reflect')
    mel = wav2melspec_db(wav, sr, n_fft, win_length, hop_length, n_mels)
    mel = normalize_db(mel, max_db=max_db, min_db=min_db)
    mel = mel.astype(np.float32)
    mel = np.expand_dims(mel, axis=0)    # single batch
    n_timesteps = sr / hop_length * duration + 1

    # send request
    channel = implementations.insecure_channel(host, int(port))
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

    # build request
    request = predict_pb2.PredictRequest()
    request.model_spec.name = 'voice_vector'
    request.model_spec.signature_name = 'predict'
    request.inputs['x'].CopyFrom(tf.contrib.util.make_tensor_proto(mel, shape=[1, n_timesteps, n_mels]))

    # asynchronous response (recommended. use this.)
    # result_future = stub.Predict.future(request, 10.0)    # timeout
    # result_future.add_done_callback(_create_rpc_callback())

    # synchronous response (NOT recommended)
    # TODO handling timeout case
    result = stub.Predict(request, 5.0)
    return result


# class _Coordinator(object):
#     def __init__(self, num_tests, concurrency):
#         self._num_tests = num_tests
#         self._concurrency = concurrency
#         self._done = 0
#         self._active = 0
#         self._condition = threading.Condition()
#
#     def inc_done(self):
#         with self._condition:
#             self._done += 1
#             self._condition.notify()
#
#     def wait_all_done(self):
#         with self._condition:
#             while self._done < self._num_tests:
#                 self._condition.wait()
#
#     def throttle(self):
#         with self._condition:
#             while self._active >= self._concurrency:
#                 self._condition.wait()
#             self._active += 1
#
#     def dec_active(self):
#         with self._condition:
#             self._active -= 1
#             self._condition.notify()


#def _create_rpc_callback():
#    def _callback(result_future):
#        """Callback function.
#
#        Args:
#            result_future: Result future of the RPC.
#        """
#        exception = result_future.exception()
#        if exception:
#            print('exception: {}'.format(exception))
#            return {'success':0}
#        else:
#            result = result_future.result()
#            response = np.array(result.outputs['prob'].float_val)
#            max_prob = np.max(response)
#            speaker_id = np.argmax(response)
#            print('{}: {}'.format(speaker_id, max_prob))
#
#    return _callback