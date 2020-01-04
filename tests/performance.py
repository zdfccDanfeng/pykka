import time

from pykka import ActorRegistry, ThreadingActor


def time_it(func):
    start = time.time()
    func()
    elapsed = time.time() - start
    print(f"{func.__name__!r} took {elapsed:.3f}s")


class SomeObject:
    pykka_traversable = False
    cat = "bar.cat"

    def func(self):
        pass


class AnActor(ThreadingActor):
    bar = SomeObject()
    bar.pykka_traversable = True

    foo = "foo"

    def __init__(self):
        super().__init__()
        self.cat = "quox"

    def func(self):
        pass


def test_direct_plain_attribute_access():
    actor = AnActor.start().proxy()
    for _ in range(10000):
        actor.foo.get()


def test_direct_callable_attribute_access():
    actor = AnActor.start().proxy()
    for _ in range(10000):
        actor.func().get()


def test_traversable_plain_attribute_access():
    actor = AnActor.start().proxy()
    for _ in range(10000):
        actor.bar.cat.get()


def test_traversable_callable_attribute_access():
    actor = AnActor.start().proxy()
    for _ in range(10000):
        actor.bar.func().get()


if __name__ == "__main__":
    try:
        time_it(test_direct_plain_attribute_access)
        time_it(test_direct_callable_attribute_access)
        time_it(test_traversable_plain_attribute_access)
        time_it(test_traversable_callable_attribute_access)
    finally:
        ActorRegistry.stop_all()
