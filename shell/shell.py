
from subprocess import Popen, PIPE
import sys
import threading
import os
import hashlib
import json

BLOCKCHAIN_FILE = 'blockchain-server.txt'


class Block(dict):
    def __init__(self, previous, data):
        dict.__init__(self, data=data)
        self['previous_hash'] = '' if previous is None else previous['hash']
        self['hash'] = self.hash()

    def hash(self):
        hash_data = self['data'] + self['previous_hash']
        hash_data = str.encode(hash_data)
        return hashlib.sha256(hash_data).hexdigest()

def main():
    os.chdir('/Users/testuser')

    blockchain = open(BLOCKCHAIN_FILE, 'w')
    currentBlock = None

    p = Popen("/bin/bash", stdin=PIPE, stdout=PIPE)
    stdin, stdout = p.stdin, p.stdout

    def watch_output(stdout_handle):
        while True:
            sys.stdout.write(stdout_handle.read(1).decode())
            sys.stdout.flush()

    t = threading.Thread(target=watch_output, args=(stdout,))
    t.start()

    while True:
        command_input = str.encode(sys.stdin.readline())
        stdin.write(command_input)
        stdin.flush()

        command_input = command_input.decode()
        currentBlock = Block(currentBlock, command_input)
        blockchain.write('{} {}'.format(json.dumps(currentBlock), command_input))
        blockchain.flush()

if __name__ == '__main__':
    main()