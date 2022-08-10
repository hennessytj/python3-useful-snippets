import os
import sys
from contextlib import contextmanager

@contextmanager
def create_test_file(path: str, contents: str):
    """Context manager used to assist the testing of file operations. It
    allows the caller to perform some action on the file as if it
    already existed without being concerned about file creation and removal.
    
    Usage:
    with create_test_file('test.txt', 'item 1, item 2\nitem3, item4'):
        with open('test.txt', 'r') as file_obj:
            for line in file_obj:
                if line.startswith('item 3'):
                    print(line)
    
    This means that when the above outer block is exited, test.txt is
    gracefully removed from the system. This should increase the velocity
    of file operation testing.
    """
    try:
        with open(path, "w") as file_handle:
            file_handle.write(contents)
    except:
        # find the actual exception which was raised
        exc = sys.exc_info()[0]
        raise exc(f"caught while attempting to create and write {path}")
    finally:
        if os.path.exists(path):
            path.close()

    try:
        # gives caller context to complete task
        yield
    finally:
        # when caller leaves with block remove this file
        os.remove(path)
