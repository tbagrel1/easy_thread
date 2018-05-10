# easy_thread

## Presentation

Easy thread is a simple way to create basic threads with Python 3.

## How to use it

### Example 1 - Print information from two sources

This example is the simplest one that can imagined: two writers are writing in two different threads on the standard output:

```python
    from easy_thread import ThreadPool

    from time import sleep
    from random import random

    def print_n(author, n):
        """Prints number from 0 to n - 1."""
        for i in range(n):
            sleep(random())
            print("[{}]: {}".format(author, i))
    ThreadPool().add(1, print_n, 1, 10).add(2, print_n, 2, 8)
```

### Example 2 - Wait for an internet query to return

In this one, an internet query is made in the background (but just waiting for it there to show how threading works):

```python
    from easy_thread import ThreadPool

    from urllib.request import urlopen
    from time import sleep

    def get_page():
        """Returns google homepage."""
        return urlopen("https://www.google.com").read()

    pool = ThreadPool()
    print("Asking for the page...")
    pool.add(0, get_page)
    count = 0
    while pool.is_running(0):
        count += 1
        print("    ...waiting for the page [{}]".format(count))
        sleep(0.01)
    if pool.has_failed(0):
        print("Unable to get the page :(")
    else:
        page = pool.get_result(0)
        print("Page received: {}".format(page[:min(20, len(page))]))
```

Note that the `main` function is runnable and contains these examples.

## Licence

This program is published under the GNU Affero General Public License.  
See `apgl_3.0.md` for more information.
