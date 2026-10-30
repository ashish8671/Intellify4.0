import json
import shutil
from pathlib import Path
import random

# ============================================================
# HRCDS -> YOLO SEGMENTATION DATASET CONVERTER
# ============================================================

SOURCE = Path(r"D:\Intellify4.0\datasets\HRCDS")
OUTPUT = Path(r"D:\Intellify4.0\datasets\HRCDS_YOLO")

CLASS_NAMES = {
    "crack": 0,
    "spalling": 1,
    "corrosion": 2,
    "exposed rebar": 3,
}

# ------------------------------------------------------------
# Create output directories
# ------------------------------------------------------------

for split in ["train", "val", "test"]:
    (OUTPUT / "images" / split).mkdir(parents=True, exist_ok=True)
    (OUTPUT / "labels" / split).mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# Convert one annotation file
# ------------------------------------------------------------

def convert_annotation(json_file, image_source_dir, split):

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    image_path_value = data.get("imagePath")

    if not image_path_value:
        print(f"Skipping {json_file.name}: imagePath missing")
        return False

    image_name = Path(image_path_value).name

    # Dataset annotations use paths such as:
    # ..\test_image\test_0001.jpg
    #
    # Therefore we search for the image inside the
    # corresponding dataset split.

    image_candidates = list(image_source_dir.rglob(image_name))

    if not image_candidates:
        print(f"Image not found for {json_file.name}: {image_name}")
        return False

    source_image = image_candidates[0]

    output_image = OUTPUT / "images" / split / image_name
    output_label = OUTPUT / "labels" / split / (
        Path(image_name).stem + ".txt"
    )

    shutil.copy2(source_image, output_image)

    image_width = data["imageWidth"]
    image_height = data["imageHeight"]

    yolo_lines = []

    for shape in data.get("shapes", []):

        label = shape.get("label", "").strip().lower()

        if label not in CLASS_NAMES:
            print(
                f"Unknown label '{label}' "
                f"in {json_file.name}"
            )
            continue

        points = shape.get("points", [])

        if len(points) < 3:
            continue

        class_id = CLASS_NAMES[label]

        normalized_points = []

        for x, y in points:

            x_norm = max(0.0, min(1.0, x / image_width))
            y_norm = max(0.0, min(1.0, y / image_height))

            normalized_points.append(x_norm)
            normalized_points.append(y_norm)

        line = (
            str(class_id)
            + " "
            + " ".join(
                f"{value:.6f}"
                for value in normalized_points
            )
        )

        yolo_lines.append(line)

    if not yolo_lines:
        print(
            f"No valid annotations for {json_file.name}"
        )
        return False

    with open(output_label, "w", encoding="utf-8") as f:
        f.write("\n".join(yolo_lines))

    return True


# ------------------------------------------------------------
# Find dataset splits
# ------------------------------------------------------------

split_mapping = {
    "train": "train",
    "val": "val",
    "test": "test",
}

total_converted = 0

for split, source_split in split_mapping.items():

    annotation_dir = SOURCE / f"{source_split}_annotations"

    if not annotation_dir.exists():
        print(
            f"WARNING: {annotation_dir} does not exist."
        )
        continue

    print()
    print("=" * 60)
    print(f"Processing {split.upper()}")
    print("=" * 60)

    json_files = sorted(annotation_dir.glob("*.json"))

    print(
        f"Found {len(json_files)} annotation files"
    )

    # The images may be stored in:
    # train_image
    # val_image
    # test_image

    image_dir = SOURCE / f"{source_split}_image"

    if not image_dir.exists():

        # Search for possible image directories
        possible_dirs = [
            SOURCE / "train_image",
            SOURCE / "val_image",
            SOURCE / "test_image",
            SOURCE / f"{source_split}_images",
            SOURCE / f"{source_split}_image",
        ]

        for candidate in possible_dirs:
            if candidate.exists():
                image_dir = candidate
                break

    converted = 0

    for json_file in json_files:

        success = convert_annotation(
            json_file,
            image_dir,
            split
        )

        if success:
            converted += 1

    print(
        f"Converted {converted}/{len(json_files)} files"
    )

    total_converted += converted


# ------------------------------------------------------------
# Create data.yaml
# ------------------------------------------------------------

yaml_content = f"""path: {OUTPUT.as_posix()}
train: images/train
val: images/val
test: images/test

names:
  0: crack
  1: spalling
  2: corrosion
  3: exposed_rebar
"""

with open(
    OUTPUT / "data.yaml",
    "w",
    encoding="utf-8"
) as f:
    f.write(yaml_content)


print()
print("=" * 60)
print("CONVERSION COMPLETE")
print("=" * 60)
print(f"Total converted: {total_converted}")
print(f"YOLO dataset: {OUTPUT}")
print()
print("Classes:")
for class_id, name in enumerate(CLASS_NAMES.keys()):
    print(f"{class_id}: {name}")

print()
print("data.yaml created successfully.")