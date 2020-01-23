"""
Periodically generates words to send over a TCP socket.
"""

import sys
import random
import socket
from threading import Thread, Event
from time import sleep


# Set of words to be used by the word generator
WORD_SET = list(set("""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed in vulputate mi. Quisque quam metus, 
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
laoreet, euismod sem sed, porta urna. Orci varius natoque penatibus."""
                    .replace(",", "")
                    .replace(".", "")
                    .replace("\n", "")
                    .split(" ")))


class Generator:
    """
    Fires up a simple word generator in a separate thread, sending words over a TCP socket.
    """

    def __init__(self, host: str = "localhost", port: int = 9999, time_interval: float = 0.05, name: str = None):
        """
        Creates a Generator object instance that transmits random words over TCP to the given target host.

        :param host: hostname (default: localhost)
        :param port: port number (default: 9999)
        :param time_interval: interval between each word (default: 0.05 s = 50 ms)
        :param name: generator identifier for debug purposes
        """

        self.__host = host
        self.__port = port
        self.__time_interval = time_interval
        self.__name = name

        self.__run = Event()
        self.__thread = Thread(target=self.__generate_words)

    def __generate_words(self) -> None:
        """
        Word generator routine to be run on a separate thread.

        :return: None
        """

        print("Thread started")
        prefix = "{name}: ".format(name=self.__name) if self.__name is not None else ""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_handle:
            sock_handle.connect((self.__host, self.__port))

            while self.__run.is_set():
                # choose a random word
                word = random.choice(WORD_SET)

                # send the word over TCP
                message = "{prefix}{word}\n".format(prefix=prefix, word=word)
                sock_handle.send(bytes(message, encoding="utf-8"))

                # wait for the given time interval
                sleep(self.__time_interval)
        print("Thread ended")

    def start(self) -> None:
        """
        Starts the word generator in a separate thread.

        :return: None
        """

        self.__run.set()
        self.__thread.start()

    def stop(self) -> None:
        """
        Kills the word generator thread.

        :return: None
        """

        self.__run.clear()
        self.__thread.join()


def generate_words(host: str = "localhost", port: int = 9999, time_interval: float = 0.05, duration: float = 2) -> None:
    """
    Creates and runs a new word generator with the given parameters for the given amount of time.

    :param host: hostname (default: localhost)
    :param port: port number (default: 9999)
    :param time_interval: interval between each word (default: 0.05 s = 50 ms)
    :param duration: amount of time the word generator should run for (default: 2 s)

    :return: None
    """

    assert 1024 < port < 65536, "Invalid port number (1024 < integer < 65536)"
    assert time_interval >= 0, "Invalid time interval (must be a positive decimal value)"
    assert duration > 0, "Invalid duration (must be a positive decimal value)"

    g = Generator(host=host,
                  port=port,
                  time_interval=time_interval)
    g.start()
    sleep(duration)
    g.stop()


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: word_generator.py <hostname> <port> <time_interval> <duration>", file=sys.stderr)
        sys.exit(-1)

    h = sys.argv[1]
    p = int(sys.argv[2])
    ti = float(sys.argv[3])
    d = float(sys.argv[4])

    generate_words(host=h,
                   port=p,
                   time_interval=ti,
                   duration=d)
