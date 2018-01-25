import json
from subprocess import Popen, PIPE

import sys

import thread

import signal

import hashlib


BLOCKCHAIN_FILE = 'blockchain.txt'


class Block(dict):
    def __init__(self, previous, data):
        dict.__init__(self, data=data)
        self['previous_hash'] = '' if previous is None else previous['hash']
        self['hash'] = self.hash()

    def hash(self):
        hash_data = self['data'] + self['previous_hash']
        return hashlib.sha256(hash_data).hexdigest()


def signal_handler(signal, frame):
    print('Exiting MagicClient')
    sys.exit(0)


def main():
    # 1. open ssh connection

    blockchain = open(BLOCKCHAIN_FILE, 'w')
    currentBlock = None

    p = Popen("cat", stdin=PIPE, stdout=PIPE)
    stdin, stdout = p.stdin, p.stdout

    def watch_output(stdout_handle):
        try:
            while True:
                sys.stdout.write(stdout_handle.read(1))
                sys.stdout.flush()
        except Exception:
            pass

    thread.start_new_thread(watch_output, (stdout,))

    while True:
        command_input = sys.stdin.readline()
        stdin.write(command_input)
        currentBlock = Block(currentBlock, command_input)
        blockchain.write('{} {}'.format(json.dumps(currentBlock), command_input))

        # 2. accept lines of input
        # 3. send them to the ssh connection
        # 4. all output is displayed as normal

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    # signal.pause()
    main()
