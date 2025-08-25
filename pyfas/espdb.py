class ESPDBFile:
    def __init__(self):
        pass

    @staticmethod
    def create_espdb(path, esp_vers, esp_label, esp_model, freq, min_rate:float, max_rate:float,
                flow_rate:list, head_per_stage:list, power:list, rate_units = 'm3/sec'):
        '''
        flow_rate - m3/day
        head_per_stage - MPa
        power - kW
        '''
        strings_to_txtfile = []
        if len(flow_rate) == len(head_per_stage) == len(power):
            for i in range(len(flow_rate)):
                strings_to_txtfile.append(str(f'{esp_vers},{esp_label},{esp_model},{freq},Calibration,Hz,' + \
                                            f'{min_rate/86400},VolumeFlow,{rate_units},{max_rate/86400},VolumeFlow,{rate_units},' +\
                                            f'{flow_rate[i]/86400},VolumeFlow,{rate_units},{head_per_stage[i]},Zlength,m,{power[i] * 0.00135962},Power,hp\n'))

        else:
            raise ValueError('Arrays must be the same legth')
        # здесь будем формировать список из строк, который надо занести в .txt

        with open(path, 'w+') as txtfile:
        # здесь уже открываем файл и пишем в него
            txtfile.write('version,label,model,frequency,type,units,min_rate,type2,units3,max_rate,type4,units5,flow_rate,type6,units7,head_per_stage,type8,units9,power,type10,units11\n')
            txtfile.writelines(strings_to_txtfile)
            txtfile.close()



if __name__ == '__main__':
    esp = ESPDBFile()
    esp.create_espdb('espdb_w200.txt',1,'LEMAZ','ESP5A-160',48.5,140,250,
             flow_rate=[0.488, 44.61, 85.89, 145.2, 168.8, 202.7, 226.3, 245.5, 290.8, 357.1],
             head_per_stage=[5.794, 5.833, 5.493, 5.225, 5.137, 4.806, 4.443, 4.092, 2.554, 0.446],
             power=[88.96, 110.4,128.9,151.8,159.5,170.7, 176.3, 176.7, 171.3,164.1])