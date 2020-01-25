"""
Simulates dynamic application load over time for testing purposes.
"""

import sys
from os.path import exists
from threading import Thread
from typing import List

from code.file_generator import generate_file


def spawn_threads(lengths: List[int], tmp_dir: str, tgt_dir: str) -> None:
    threads = [Thread(target=generate_file,
                      kwargs={"length": file_len,
                              "tmp_dir": tmp_dir,
                              "tgt_dir": tgt_dir}
                      )
               for file_len in range(0, len(lengths))]

    print("Spawning threads...")
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

    spawn_threads(lengths=[1],
                  tmp_dir=tmp,
                  tgt_dir=tgt)
