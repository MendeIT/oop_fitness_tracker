from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    TEXT = (
        'Тип тренировки: {}; '
        'Длительность: {:.3f} ч.; '
        'Дистанция: {:.3f} км; '
        'Ср. скорость: {:.3f} км/ч; '
        'Потрачено ккал: {:.3f}.'
    )

    def get_message(self) -> str:
        """"Получить информацию о тренировке."""
        return self.TEXT.format(*asdict(self).values())


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: float = 1000  # Из метров в километры.
    H_IN_MIN: float = 60  # Из часов в минуты.
    LEN_STEP: float = 0.65  # Длина шага в метрах.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action  # Число шагов, гребков.
        self.duration = duration  # Время (Продолжительность) тренировки.
        self.weight = weight  # Вес спортсмена.

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определите get_spent_calories в %s.' % (type(self). __name__)
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self). __name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self, action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action,
                         duration,
                         weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * (self.duration * self.H_IN_MIN))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEF_1: float = 0.035  # Классовый коэфицент.
    COEF_2: float = 0.029  # Классовый коэфицент.
    KM_H_IN_M_S: float = 0.278  # Из км/ч в м/с.
    CM_IN_M: float = 100  # Из сантиметров в метры.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при ходьбе."""
        return ((self.COEF_1 * self.weight
                 + ((self.get_mean_speed() * self.KM_H_IN_M_S)**2
                    / (self.height / self.CM_IN_M))
                 * self.COEF_2 * self.weight)
                * (self.duration * self.H_IN_MIN))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # Длина одного гребка в м.
    NUMBER_1: float = 1.1  # Классовый коэфицент.
    NUMBER_2: float = 2  # Классовый коэфицент.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int):
        super().__init__(action,
                         duration,
                         weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self):
        """Получить количество затраченных калорий при плавании."""
        return ((self.get_mean_speed() + self.NUMBER_1)
                * self.NUMBER_2 * self.weight * self.duration)

    def get_mean_speed(self):
        """Получить среднюю скорость движения при плавании в км/ч."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    # Создает экземпляр класса Traning.
    workout_code: dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in workout_code:
        return workout_code[workout_type](*data)
    else:
        print('Данный тип тренировки неизвестен. '
              'Попробуйте походить, поплавать или бег.')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
