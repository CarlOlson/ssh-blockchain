
from subprocess import Popen, PIPE
import sys
import _thread

def main():
    p = Popen("/bin/sh", stdin=PIPE, stdout=PIPE)
    stdin, stdout = p.stdin, p.stdout

    def watch_output(stdout_handle):
        try:
            while True:
                sys.stdout.write(stdout_handle.read(1))
                sys.stdout.flush()
        except Exception:
            pass

    _thread.start_new_thread(watch_output, (stdout,))

    while True:
        command_input = str.encode(sys.stdin.readline())
        stdin.write(command_input)

if __name__ == '__main__':
    main()