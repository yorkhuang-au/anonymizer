import os
import sys
import string
import random
from anonymizer import anonymizer as ano


def main():
    if len(sys.argv) == 4:
        secret = sys.argv[1]
        input_filename = sys.argv[2]
        output_filename = sys.argv[3]
    elif len(sys.argv) == 2:
        secret = sys.argv[1]
        input_filename = ano.generate_source_csv(1000)
        output_filename = os.path.join(os.path.dirname(input_filename), f"out_{os.path.basename(input_filename)}")
    elif len(sys.argv) == 1:
        # create a random 5 chars string as secret
        secret = ''.join((random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(5)))
        input_filename = ano.generate_source_csv(1000)
        output_filename = os.path.join(os.path.dirname(input_filename), f"out_{os.path.basename(input_filename)}")
    else:
        ano.usage()
        sys.exit(1)

    ano.anonymize_csv(secret, input_filename, output_filename)


if __name__ == '__main__':
    main()
