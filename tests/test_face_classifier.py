import unittest
import os
import sys
this_script_path = os.path.abspath(__file__)
this_script_folder = os.path.dirname(this_script_path)
sys.path.insert(1, os.path.join(this_script_folder, '..', 'ezfaces'))
from face_classifier import FaceClassifier
import numpy as np


class TestUM(unittest.TestCase):

    def test_train_with_olivetti(self):
        fc = FaceClassifier()
        self.assertEqual(len(fc.data.shape), 2)
        # data stored as 64*64 row vectors
        self.assertEqual(fc.data.shape[1], 64*64)
        # Olivetti data contain 40 subjects
        self.assertEqual(len(np.unique(fc.labels)), 40)
        fc.train()
        # their coordinates in eigenface space as a matrix (.W)
        self.assertEqual(len(fc.W.shape), 2)


    def test_train_with_subject(self):
        img_dir = os.path.join(this_script_folder, 'images_yale')
        fc = FaceClassifier()
        fc.add_img_data(img_dir)
        # data stored as 64*64 row vectors
        self.assertEqual(fc.data.shape[1], 64*64)
        # 40 + 1 subjects
        self.assertEqual(len(np.unique(fc.labels)), 41)
        fc.train()
        # their coordinates in eigenface space as a matrix (.W)
        self.assertEqual(len(fc.W.shape), 2)


    def test_benchmark(self):
        img_dir = os.path.join(this_script_folder, 'images_yale')
        fc = FaceClassifier(ratio = .725)
        fc.add_img_data(img_dir)
        fc.benchmark()
        self.assertNotEqual(fc.classification_report, None)
        print(fc.classification_report)
        fc.benchmark(imshow=True, wait_time=0.8, which_labels=[0, 5, 13, 28, 40])


    def test_export_import(self):
        img_dir = os.path.join(this_script_folder, 'images_yale')
        fc = FaceClassifier()
        fc.add_img_data(img_dir)
        # write as pickle files
        fc.export()

        fc2 = FaceClassifier(data_pkl = '/tmp/data.pkl', target_pkl = '/tmp/labels.pkl')
        self.assertEqual(len(np.unique(fc2.labels)), 41)


    def test_show_album(self):
        fc = FaceClassifier()
        fc.show_album(wait_time=.1)


if __name__ == '__main__':
    unittest.main()
