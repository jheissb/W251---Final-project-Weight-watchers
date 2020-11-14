import pandas as pd
import numpy as np

from glob import glob

import config
from utility import get_index_of_digit, get_face_encoding, save_model, load_model
from model import train_test_splits, train_bmi_model, predict_bmi


# todo: add the option of predicting from existing model
# todo: run the pipeline
# todo: figure out a place to store the prediction images

def main():
    profile_df = pd.read_csv(config.IMGS_INFO_FILE)

    all_files = glob(config.IMGS_DIR + "/*")
    # grab photos only
    all_jpgs = sorted([img for img in all_files if ".jpg" in img or ".jpeg" in img or "JPG" in img])
    print("Total {} photos ".format(len(all_jpgs)))

    id_path = [(p(images).stem[:(get_index_of_digit(p(images).stem))], images) for images in all_jpgs]
    image_df = pd.DataFrame(id_path, columns=['ID', 'path'])
    data_df = image_df.merge(profile_df)
    data_df.to_csv("full_df.csv")

    # extract face embedding
    all_faces = []
    for images in data_df.path:
        face_enc = get_face_encoding(images)
        all_faces.append(face_enc)

    # get training data matrix
    X = np.array(all_faces)

    # get all labels
    y_height = data_df.height.values
    y_weight = data_df.weight.values
    y_bmi = data_df.bmi.values

    X_train, X_test, y_height_train, y_height_test, y_weight_train, y_weight_test, y_bmi_train, y_bmi_test = \
        train_test_splits(X, y_height, y_weight, y_bmi)

    # train model
    bmi_model = train_bmi_model(X_train, y_bmi_train, X_test, y_bmi_test)
    save_model(bmi_model, config.OUTPUT_MODEL_DIR, config.OUTPUT_MODEL_NAME)

    bmi_model = load_model(config.OUTPUT_MODEL_DIR, config.OUTPUT_MODEL_NAME)

    # predict bmi
    bmi_list = [predict_bmi(x, bmi_model) for x in data_df["path"]]


if __name__ == "__main__":
    main()
