import argparse
import time

from PIL import Image
from PIL import ImageDraw

import detect
import tflite_runtime.interpreter as tflite
import platform

class TensorFlowPipeline:
    EDGETPU_SHARED_LIB = {
      'Linux': 'libedgetpu.so.1',
      'Darwin': 'libedgetpu.1.dylib',
      'Windows': 'edgetpu.dll'
    }[platform.system()]

    model = models/mobilenet_ssd_v2_coco_quant_postprocess.tflite
    label = models/coco_labels.txt

    def process(self, source):
      interpreter = make_interpreter(args.model)
      interpreter.allocate_tensors()

      image = Image.open(args.input)
      scale = detect.set_input(interpreter, image.size,
                               lambda size: image.resize(size, Image.ANTIALIAS))

      start = time.perf_counter()
      interpreter.invoke()
      inference_time = time.perf_counter() - start
      objs = detect.get_output(interpreter, args.threshold, scale)
      print('%.2f ms' % (inference_time * 1000))

      return objs

    def load_labels(path, encoding='utf-8'):
      """Loads labels from file (with or without index numbers).
      Args:
        path: path to label file.
        encoding: label file encoding.
      Returns:
        Dictionary mapping indices to labels.
      """
      with open(path, 'r', encoding=encoding) as f:
        lines = f.readlines()
        if not lines:
          return {}

        if lines[0].split(' ', maxsplit=1)[0].isdigit():
          pairs = [line.split(' ', maxsplit=1) for line in lines]
          return {int(index): label.strip() for index, label in pairs}
        else:
          return {index: line.strip() for index, line in enumerate(lines)}


    def make_interpreter(model_file):
      model_file, *device = model_file.split('@')
      return tflite.Interpreter(
          model_path=model_file,
          experimental_delegates=[
              tflite.load_delegate(EDGETPU_SHARED_LIB,
                                   {'device': device[0]} if device else {})
          ])


    def draw_objects(draw, objs, labels):
      """Draws the bounding box and label for each object."""
      for obj in objs:
        bbox = obj.bbox
        draw.rectangle([(bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymax)],
                       outline='red')
        draw.text((bbox.xmin + 10, bbox.ymin + 10),
                  '%s\n%.2f' % (labels.get(obj.id, obj.id), obj.score),
                  fill='red')



