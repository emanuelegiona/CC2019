"""
Periodically generates words to send over a TCP socket.
"""

import sys
from os.path import join, exists
from shutil import move
from time import time


# Set of words to be used by the word generator
TEXT = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed in vulputate mi. Quisque quam metus, 
elementum a sapien id, interdum dignissim dui. Nam ut mi placerat urna sodales ultricies et ut elit. Pellentesque 
aliquam venenatis arcu a placerat. Duis scelerisque malesuada porttitor. Nam et tristique diam, et pharetra diam. 
Quisque quis faucibus turpis. Nullam ultrices luctus nibh at auctor. Vestibulum fermentum ligula sit amet mi tempus 
tempor. Sed pellentesque, sapien sit amet dictum tincidunt, metus urna dapibus justo, id fringilla felis ex et elit. 
Donec in mi nulla. Phasellus facilisis, diam sit amet lobortis ultrices, ante neque aliquam sem, pretium tincidunt 
felis lectus dignissim justo. Morbi molestie scelerisque faucibus. Vivamus sed varius magna. Curabitur aliquam 
feugiat ullamcorper. 

Nunc porttitor vehicula arcu, vitae posuere urna elementum feugiat. Maecenas lacinia tortor risus. Duis pretium 
blandit nisi, cursus imperdiet nisl imperdiet sed. Aenean in vestibulum purus. Quisque dictum, sem non fringilla 
commodo, ante sapien lacinia neque, in fringilla neque dui sed risus. Sed a enim eget enim lacinia vehicula sed nec 
felis. Curabitur consectetur malesuada eros. Suspendisse vitae vulputate massa. Sed sodales turpis et risus aliquet 
vehicula et vel lorem. Sed in metus eu ipsum semper faucibus. Aenean mollis augue in imperdiet fringilla. Proin nec 
ultricies purus, sit amet sodales sapien. 

Vivamus sed nunc massa. Duis fringilla dignissim justo nec euismod. Vivamus interdum libero dui, sagittis convallis 
nunc blandit ut. Suspendisse suscipit rutrum vehicula. Aenean placerat eget ante quis euismod. Fusce eget nunc 
laoreet, euismod sem sed, porta urna. Orci varius natoque penatibus."""\
    .replace(",", "")\
    .replace(".", "")\
    .replace("\n", "")


def generate_file(length: int = 1, tmp_dir: str = "tmp/", tgt_dir: str = "data/", quiet: bool = False) -> None:
    """
    Creates a an arbitrary length file in a temporary directory, then moves it to the target directory.

    :param length: number of repetitions of TEXT to be contained in the generated file
    :param tmp_dir: path to the temporary directory
    :param tgt_dir: path to the target directory
    :param quiet: if True, no output to the standard output
    """

    timestamp = str(time()).replace(".", "")
    filename = "text_{timestamp}.txt".format(timestamp=timestamp)
    tmp_path = join(tmp_dir, filename)
    tgt_path = join(tgt_dir, filename)

    # file creation
    try:
        if not quiet:
            print("Creating file...")

        with open(tmp_path, "w", encoding="utf-8"):
            pass

        with open(tmp_path, "a", encoding="utf-8") as file:
            for i in range(0, length):
                file.write(TEXT)
                file.write(" ")
                file.flush()

        if not quiet:
            print("Done.")

    except Exception as e:
        if not quiet:
            print("Error during file creation ({msg}).".format(msg=str(e)))

        return

    # file moving
    try:
        if not quiet:
            print("Moving file...")
        move(tmp_path, tgt_path)

        if not quiet:
            print("Done.")

    except Exception as e:
        if not quiet:
            print("Error during file moving ({msg}).".format(msg=str(e)))

        return


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: file_generator.py <length> <tmp_dir> <tgt_dir>", file=sys.stderr)
        sys.exit(-1)

    file_len = int(sys.argv[1])
    tmp = sys.argv[2]
    tgt = sys.argv[3]

    assert file_len > 0, "Length should be at least 1"
    assert exists(tmp), "Temporary directory does not exist"
    assert exists(tgt), "Target directory does not exist"

    generate_file(length=file_len,
                  tmp_dir=tmp,
                  tgt_dir=tgt)
