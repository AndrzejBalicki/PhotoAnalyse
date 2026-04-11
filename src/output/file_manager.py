import os
import shutil
import config

def classify(score):
    if score >= config.TOP_THRESHOLD:
        return "TOP"
    elif score >= config.MID_THRESHOLD:
        return "MID"
    return "LOW"


def handle_output(file, score, is_best):

    category = classify(score)

    if config.MODE == "copy":
        out_dir = os.path.join(config.OUTPUT_DIR, category)
        os.makedirs(out_dir, exist_ok=True)
        shutil.copy(file, out_dir)

    elif config.MODE == "rename":
        dirname = os.path.dirname(file)
        basename = os.path.basename(file)

        prefix = f"{int(score)}"
        if is_best:
            prefix = "BEST_" + prefix

        new_name = os.path.join(dirname, f"{prefix}-{basename}")
        os.rename(file, new_name)