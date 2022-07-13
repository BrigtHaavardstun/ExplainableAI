
import cv2
from local_utils import reconstruct
import tensorflow.compat.v1 as tf
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from tensorflow import keras
import tensorflow as tf
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2
import numpy as np


def convert_keras_to_graph(model):
    model = keras.models.load_model('models/wpod_net_all_in_one.h5')

    # Convert Keras model to ConcreteFunction
    full_model = tf.function(lambda x: model(x))
    full_model = full_model.get_concrete_function(
        x=tf.TensorSpec(model.inputs[0].shape, model.inputs[0].dtype))

    # Get frozen ConcreteFunction
    frozen_func = convert_variables_to_constants_v2(full_model)
    frozen_func.graph.as_graph_def()

    # inspect the layers operations inside your frozen graph definition and see the name of its input and output tensors
    layers = [op.name for op in frozen_func.graph.get_operations()]
    print("-" * 50)
    print("Frozen model layers: ")
    for layer in layers:
        print(layer)

    print("-" * 50)
    print("Frozen model inputs: ")
    print(frozen_func.inputs)
    print("Frozen model outputs: ")
    print(frozen_func.outputs)

    # Save frozen graph from frozen ConcreteFunction to hard drive
    # serialize the frozen graph and its text representation to disk.
    tf.io.write_graph(graph_or_graph_def=frozen_func.graph,
                      logdir="./frozen_models",
                      name="simple_frozen_graph.pb",
                      as_text=False)

    # Optional
    tf.io.write_graph(graph_or_graph_def=frozen_func.graph,
                      logdir="./frozen_models",
                      name="simple_frozen_graph.pbtxt",
                      as_text=True)

    model.summary()


def preprocess_image(image_path, resize=False):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img / 255
    if resize:
        img = cv2.resize(img, (224, 224))
    return img


def get_image(image_path, sess, Dmax=608, Dmin=608):
    vehicle = preprocess_image(image_path)
    ratio = float(max(vehicle.shape[:2])) / min(vehicle.shape[:2])
    side = int(ratio * Dmin)
    bound_dim = min(side, Dmax)
    processed_image, Iresized = prepare_image_for_tf_inferencing(
        vehicle, bound_dim)
    infrencing = sess.run(output_tensor, {'x:0': processed_image})
    np_inferencing = np.squeeze(infrencing)
    _, LpImg, _, cor = detect_lp_tf(
        Iresized, np_inferencing, vehicle, lp_threshold=0.5)
    return vehicle, LpImg, cor


def prepare_image_for_tf_inferencing(vehicle, bound_dim):
    min_dim_img = min(vehicle.shape[:2])
    factor = float(bound_dim) / min_dim_img
    w, h = (np.array(vehicle.shape[1::-1],
            dtype=float) * factor).astype(int).tolist()
    Iresized = cv2.resize(vehicle, (w, h))
    T = Iresized.copy()
    T = T.reshape((1, T.shape[0], T.shape[1], T.shape[2]))
    return T, Iresized


def detect_lp_tf(Iresized, np_inferencing, I, lp_threshold):
    L, TLp, lp_type, Cor = reconstruct(
        I, Iresized, np_inferencing, lp_threshold)
    return L, TLp, lp_type, Cor


# Loading model
sess = tf.InteractiveSession()
frozen_graph = "./frozen_models/simple_frozen_graph.pb"
with tf.gfile.GFile(frozen_graph, "rb") as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
sess.graph.as_default()
tf.import_graph_def(graph_def)
# Frozen model inputs:
# [<tf.Tensor 'x:0' shape=(None, None, None, 3) dtype=float32>]
# Frozen model outputs:
# [<tf.Tensor 'Identity:0' shape=(None, None, None, 8) dtype=float32>]
input_tensor = sess.graph.get_tensor_by_name("x:0")
output_tensor = sess.graph.get_tensor_by_name("Identity:0")
print("Tensor Input : ", input_tensor)
print("Tensor Output: ", output_tensor)
print("..... Extracing Number Plate .......")

test_image_path = "dataset/plate5.jpeg"
vehicle, LpImg, cor = get_plate(test_image_path, sess)


fig = plt.figure(figsize=(12, 6))
grid = gridspec.GridSpec(ncols=2, nrows=1, figure=fig)
fig.add_subplot(grid[0])
plt.axis(False)
plt.imshow(vehicle)
grid = gridspec.GridSpec(ncols=2, nrows=1, figure=fig)
fig.add_subplot(grid[1])
plt.axis(False)
plt.imshow(LpImg[0])
