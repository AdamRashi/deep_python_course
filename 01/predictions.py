class SomeModel:
    def predict(self, message: str) -> float:
        # реализация не важна
        pass


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:

    if bad_thresholds >= good_thresholds:
        raise ValueError('Good threshold should be higher than bad threshold')
    if bad_thresholds < 0 or good_thresholds > 1:
        raise ValueError('Both thresholds should be in interval [0; 1]')

    mood_rate = model.predict(message)
    if mood_rate <= bad_thresholds:
        return 'неуд'
    if mood_rate >= good_thresholds:
        return 'отл'
    return 'норм'
