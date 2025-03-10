from datetime import date
from api.oilcase_x import AvailableDatesDTO, AvailablePropertyDTO


def get_available_properties_mock():
    availableDate1 = AvailableDatesDTO(
        date(2026, 5, 13),
        0,
        [1, 2, 5, 6, 7],
        [1, 2, 5, 15, 18]
    )
    availableDate2 = AvailableDatesDTO(
        date(2027, 9, 30),
        1,
        [],
        []
    )
    availableDate3 = AvailableDatesDTO(
        date(2028, 12, 30),
        2,
        list(range(0, 23)),
        list(range(0, 17))
    )

    return [
        AvailablePropertyDTO('PRESSURE', 'Пластовое давление',
                             [availableDate1, availableDate2, availableDate3],
                             True),

        AvailablePropertyDTO('ROIP', 'Остаточные запасы нефти',
                             [availableDate1, availableDate2, availableDate3],
                             True),

        AvailablePropertyDTO('SOIL', 'Нефтенасыщенность',
                             [availableDate1, availableDate2, availableDate3],
                             True),

        AvailablePropertyDTO('SGAS', 'Газонасыщенность', [
            availableDate3], True),

        AvailablePropertyDTO('SWAT', 'Водонасыщенность', [
            availableDate3], True),

        AvailablePropertyDTO('PORO', 'Пористость', [
            availableDate3], False),

        AvailablePropertyDTO('PERMX', 'Проницаемость X', [
            availableDate3], False),

        AvailablePropertyDTO('PERMY', 'Проницаемость Y', [
            availableDate3], False),

        AvailablePropertyDTO('PERMZ', 'Проницаемость Z', [
            availableDate3], False),

        AvailablePropertyDTO('SEISMIC', 'Сейсмика', [
            availableDate1], False),
    ]
