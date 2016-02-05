import numpy as np
import pyfas as fa

class RU():
    def __init__(self, fname):
        self.tpl = fa.Tpl(fname)

    def surge_calc(self, drain=0):
        if self.qlt:
            self.tpl.extract(self.qlt)
            time = self.tpl.time
            qlt = self.tpl.data[self.qlt]
            surge = []
            for idx, (ts, liq_prod) in enumerate(zip(time, qlt)):
                if idx != 0:
                    dt = ts - time[idx-1]
                    avg_liq_rate = (liq_prod + qlt[idx-1])/2
                    liq_acc = (avg_liq_rate - drain) * dt
                    surge.append(liq_acc)
            return surge
        else:
            print("Please specify the qlt variable")
