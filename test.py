from tensorflow.python.client import device_lib
import tensorflow as tf
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


print(tf.__version__)
print('A: ', tf.test.is_built_with_cuda)
print('B: ', tf.test.gpu_device_name())
local_device_protos = device_lib.list_local_devices()
([x.name for x in local_device_protos if x.device_type == 'GPU'],
 [x.name for x in local_device_protos if x.device_type == 'CPU'])
