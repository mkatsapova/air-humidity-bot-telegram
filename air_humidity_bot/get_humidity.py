from air_humidity_bot.table_humidity import humidity

# for example, can be deleted!!!
# change "round (" to "myround (") without changing the parameter values.
# def myround(x, prec=2, base=.05):
#   return round(base * round(float(x)/base),prec)

def special_round(x, base=0.5):
    return base * round(x/base)


def get_humidity(temp_dry, delta_temp):
    temp_dry = round(temp_dry)
    delta_temp = special_round(delta_temp)
    result = '...can`t be defined :( invalid data, result is not available'
    for key in humidity.keys():
        if key == tuple((temp_dry, delta_temp)):
            result = str(humidity[key]) + '%'
    #print(result)
    return result




if __name__ == '__main__':
    get_humidity(21.5, 18)
    get_humidity(21.5, 2.5)
    get_humidity(21.5, 2.2)
