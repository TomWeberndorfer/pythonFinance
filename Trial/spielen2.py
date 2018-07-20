import abc

from DataReading.NewsDataContainerDecorator import NewsDataContainerDecorator
from DataReading.StockDataContainer import StockDataContainer


class Car(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def assemble(self):
        pass


class BasicCar(Car):
    def assemble(self):
        print("Basic Car assembled.")


class CarDecorator(Car):
    def __init__(self, car):
        self.car = car

    def assemble(self):
        self.car.assemble()


class SportsCar(CarDecorator):
    def __init__(self, car):
        super(SportsCar, self).__init__(car)

    def assemble(self):
        super(SportsCar, self).assemble()
        print("Adding features of Sports Car.")


class LuxuryCar(CarDecorator):
    def __init__(self, car):
        super(LuxuryCar, self).__init__(car)

    def assemble(self):
        super(LuxuryCar, self).assemble()
        print("Adding features of Luxury Car.")


if __name__ == '__main__':
    sports_car = SportsCar(BasicCar())
    sports_car.assemble()
    print("-----")

    sports_luxury_car = SportsCar(LuxuryCar(BasicCar()))
    sports_luxury_car.assemble()

    container = StockDataContainer("test1", "t1", "en")
    print (str(container.get_names_and_values()))

    news_dec = NewsDataContainerDecorator(container, "111", "0.9", "test news", "99")
    print (str(news_dec.get_names_and_values()))