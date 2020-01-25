"""
Simulates dynamic application load over time for testing purposes.
"""

import sys
from os.path import exists
from threading import Thread
from typing import List
from time import sleep

from file_generator import generate_file


# files have dynamic length (in terms of repetitions of the TEXT sample)
FILE_LENGTHS = [length for length in range(10, 501)]


# application load pattern: from 1 to 100 threads writing files simultaneously
LOAD_PATTERN = [generators for generators in range(1, 110, 10)]
inverse_pattern = LOAD_PATTERN.copy()
inverse_pattern.reverse()
LOAD_PATTERN = LOAD_PATTERN + inverse_pattern
LOAD_PATTERN = LOAD_PATTERN


def spawn_threads(lengths: List[int], tmp_dir: str, tgt_dir: str) -> None:
    """
    Spawns a number of threads, each writing a file with the length specified in the 'lengths' argument.
    Threads execute the 'generate_file' function from 'file_generator.py'.

    :param lengths: list of file lengths; the number of threads spawned is equal to the length of this argument
    :param tmp_dir: path to the temporary directory
    :param tgt_dir: path to the target directory
    """

    threads = [Thread(target=generate_file,
                      kwargs={"length": file_len,
                              "tmp_dir": tmp_dir,
                              "tgt_dir": tgt_dir}
                      )
               for file_len in lengths]

    print("Spawning {num} threads...".format(num=len(lengths)))
    for thread in threads:
        thread.start()

    print("Waiting for execution...")
    for thread in threads:
        thread.join()

    print("Execution completed.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: benchmark.py <tmp_dir> <tgt_dir>", file=sys.stderr)
        sys.exit(-1)

    tmp = sys.argv[1]
    tgt = sys.argv[2]

    assert exists(tmp), "Temporary directory does not exist"
    assert exists(tgt), "Target directory does not exist"

    print("\nStarting benchmarking...")

    for threads_number in LOAD_PATTERN:
        print("")
        index = min(len(FILE_LENGTHS)-1, int(threads_number*5))
        spawn_threads(lengths=[FILE_LENGTHS[index]] * threads_number,
                      tmp_dir=tmp,
                      tgt_dir=tgt)
        sleep(5)

    print("\nBenchmarking completed.")
