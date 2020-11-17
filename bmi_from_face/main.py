import pandas as pd
import numpy as np
import time
import os

from glob import glob
from pathlib import Path

import config
from utility import get_index_of_digit, get_face_encoding, save_model, load_model
from model import train_test_splits, train_bmi_model, predict_bmi


def main():
    val1 = input("Prediction only? [y/n]")
    if val1 == "y":
        print("loading trained bmi model...")
        time.sleep(2)
        model = load_model(config.OUTPUT_MODEL_DIR, config.OUTPUT_MODEL_NAME)
        print("running prediction...")
        time.sleep(2)
        bmi_dict = predict_bmi(config.PREDICTION_IMG_PATH, model)
        print(bmi_dict)
    if val1 == "n":
        val2 = input("Are you sure? [y/n]")
        if val2 == "y":
            print("training model...")
            profile_df = pd.read_csv(config.IMGS_INFO_FILE)

            all_files = glob(config.IMGS_DIR + "/*")
            # grab photos only
            all_jpgs = sorted([img for img in all_files if ".jpg" in img or ".jpeg" in img or "JPG" in img or ".png" in img])
            print("Total {} photos ".format(len(all_jpgs)))

            id_path = [(Path(images).stem[:(get_index_of_digit(Path(images).stem))], images) for images in all_jpgs]
            print(id_path)
            image_df = pd.DataFrame(id_path, columns=['ID', 'path'])
            print(image_df)
            data_df = image_df.merge(profile_df)
            data_df.to_csv(os.path.join(config.OUTPUT_TRAINING_DATA_DIR, config.OUTPUT_TRAINING_DATA_FILE))

            # extract face embedding
            all_faces = []
            for images in data_df.path:
                print(images)
                face_enc = get_face_encoding(images)
                all_faces.append(face_enc)
            print(all_faces[0])

            # get training data matrix
            X = np.array(all_faces)

            # get all labels
            y_height = data_df.height.values
            y_weight = data_df.weight.values
            y_bmi = data_df.bmi.values

            X_train, X_test, y_height_train, y_height_test, y_weight_train, y_weight_test, y_bmi_train, y_bmi_test = \
                train_test_splits(X, y_height, y_weight, y_bmi)

            # train bmi model
            bmi_model = train_bmi_model(X_train, y_bmi_train, X_test, y_bmi_test)
            print("saving trained model...")
            save_model(bmi_model, config.OUTPUT_MODEL_DIR, config.OUTPUT_MODEL_NAME)
        if val2 == "n":
            print("Process completed. If you'd like to run prediction only, please rerun the program.")


if __name__ == "__main__":
    main()
