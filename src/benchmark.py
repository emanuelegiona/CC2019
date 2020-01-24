"""
Simulates dynamic application load over time for testing purposes.
"""

import sys
from src.word_generator import generate_words


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: benchmark.py <hostname> <port>", file=sys.stderr)
        sys.exit(-1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    # 10 words per second, for 2 minutes
    generate_words(host=host,
                   port=port,
                   time_interval=0.1,
                   duration=120)

    # 500 words per second, for 5 minutes --> scaling up should occur here
    generate_words(host=host,
                   port=port,
                   time_interval=0.002,
                   duration=300)

    # 100 words per second, for 2 minutes --> scaling down should occur here
    generate_words(host=host,
                   port=port,
                   time_interval=0.01,
                   duration=120)

    # 10 words per second, for 2 minutes
    generate_words(host=host,
                   port=port,
                   time_interval=0.1,
                   duration=120)
