import os
import datetime
import shutil

# Format of the image file
FORMAT = "WIN_{0}{1:02d}{2:02d}_{3:02d}_{4:02d}_{5:02d}{6}"

# Image file extension
EXTENSION = ".jpg"

# Folder where the timelapse images are stored
IMAGES_DIR = r"images"

# Folder where the sampled images are stored
SAMPLES_DIR = r"samples"

# Sampled image interval
TIMEDELTA = datetime.timedelta(minutes=15)

FIRST = 0
LAST = -1


def extract_filename(filename):
    """
    Extract the filename of the image without the file extension
    :param filename:
    :return:
    """
    return os.path.splitext(filename)[0]


def extract_timestamp(filename, split_char="_"):
    """
    Extract the timestamp from the filename
    :param filename:
    :param split_char:
    :return:
    """
    filename = extract_filename(filename)
    sections = filename.split(split_char)
    timestamp = dict()
    timestamp["year"] = int(sections[1][:4])
    timestamp["month"] = int(sections[1][4:6])
    timestamp["day"] = int(sections[1][-2:])
    timestamp["hour"] = int(sections[2])
    timestamp["minute"] = int(sections[3])
    timestamp["second"] = int(sections[4])

    return datetime.datetime(**timestamp)


def sample_images(image_timestamps, timedelta=TIMEDELTA, position=LAST):
    """
    Sample the image every timedelta
    :param image_timestamps:
    :param timedelta:
    :param position:
    :return:
    """
    image_timestamps.sort()

    index = 0
    attempts = 1
    timestamp_to_find = image_timestamps[index]
    samples = list()
    while True:
        try:
            matches = [
                item for item in image_timestamps
                if item.replace(second=0) == timestamp_to_find.replace(
                    second=0)
            ]
            samples.append(matches[position])
            # image_timestamps = image_timestamps[index::]
            # index = image_timestamps.index(matches[position])
            timestamp_to_find = matches[position] + timedelta

            attempts = 1
        except IndexError:
            attempts += 1
            if timestamp_to_find < max(image_timestamps):
                timestamp_to_find = timestamp_to_find + timedelta
            else:
                return samples


def recreate_filename(timestamp, extension=EXTENSION):
    """
    Recreate the image filename
    :param timestamp:
    :param extension:
    :return:
    """
    return FORMAT.format(timestamp.year, timestamp.month, timestamp.day,
                         timestamp.hour, timestamp.minute, timestamp.second,
                         extension)


def copy_samples(file_list, extension=EXTENSION):
    """
    Copy the sampled images from images folder to samples folder
    :param file_list:
    :param extension:
    :return:
    """
    images = [f for f in file_list if f.endswith(extension)]
    image_timestamps = list(map(extract_timestamp, images))
    samples = sample_images(image_timestamps)

    if not os.path.exists(SAMPLES_DIR):
        os.makedirs(SAMPLES_DIR)

    for s in samples:
        filename = recreate_filename(s, extension)
        print(filename)
        source = os.path.join(IMAGES_DIR, filename)
        destination = os.path.join(SAMPLES_DIR, filename)

        shutil.copy(source, destination)


try:
    files = os.listdir(IMAGES_DIR)
    copy_samples(files)
except IndexError:
    print("Copy the timelapse images to images folder")
