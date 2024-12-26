from catboost import CatBoostClassifier
import os

def get_model_path(path: str) -> str:
    if (
        os.environ.get("IS_LMS") == "1"
    ):  # проверяем где выполняется код в лмс, или локально. Немного магии
        MODEL_PATH = "/workdir/user_input/model"
    else:
        MODEL_PATH = path
    return MODEL_PATH


def load_models():
    model_path = get_model_path(
        "catboost_model"
    )  # Assuming the model file is in the same directory
    from_file = CatBoostClassifier()
    model = from_file.load_model(model_path)
    return model
