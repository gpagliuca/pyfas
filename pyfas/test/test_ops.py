from pyfas import RU

def test_init():
    ru = RU("11_2022_BD.tpl")
    ru.qlt = 10
    ru.surge_calc()
    #assert ru.surge[0] == 0
