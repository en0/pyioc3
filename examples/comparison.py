from abc import ABC, abstractmethod
from contextlib import contextmanager


class Stereo(ABC):
    @abstractmethod
    @contextmanager
    def play(self):
        ...


class StockStereo(ABC):
    @contextmanager
    def play(self):
        try:
            yield
        finally:
            print("with tunes...")


class HighEndStereo(ABC):
    @contextmanager
    def play(self):
        try:
            yield
        finally:
            print("with punchy tunes...")


class Car:
    def __init__(self, stereo: Stereo):
        self._stereo = stereo

    def drive_to_work(self):
        print("Start the car")
        with self._stereo.play():
            print("Drive to work")


print("\n== Buill a Car manually ====================")
stereo = StockStereo()
car = Car(stereo)
car.drive_to_work()


print("\n== Buill a Car with IoC ====================")
from pyioc3 import StaticContainerBuilder  # noqa: E402

ioc = StaticContainerBuilder().bind(Car).bind(Stereo, StockStereo).build()
car = ioc.get(Car)
car.drive_to_work()


print("\n== Build a Car with a Car Builder ==========")
from pyioc3.builder import BuilderBase  # noqa: E402
from pyioc3.interface import ProviderBinding  # noqa: E402


class CarBuilder(BuilderBase[Car]):
    def __init__(self):
        super().__init__(target_t=Car, bindings=[ProviderBinding(Stereo, StockStereo)])

    def with_high_end_stereo(self):
        self.using_provider(Stereo, HighEndStereo)
        return self


car = CarBuilder().build()
car.drive_to_work()


print("\n== Build a new Car with the same Builder ===")
car = CarBuilder().with_high_end_stereo().build()
car.drive_to_work()

print("\n== Build a Car with a Vehicle Builder ==========")
from pyioc3.builder import BuilderBase  # noqa: E402


class Vehicle(ABC):
    @abstractmethod
    def drive_to_work(self):
        ...


class VehicleBuilder(BuilderBase[Vehicle]):
    def with_stock_stereo(self):
        self.using_provider(Stereo, StockStereo)
        return self

    def with_high_end_stereo(self):
        self.using_provider(Stereo, HighEndStereo)
        return self


car = VehicleBuilder(Car).with_high_end_stereo().build()
car.drive_to_work()
