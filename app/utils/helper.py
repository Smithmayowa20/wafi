

def currency_conversion(from_curr,to_curr,amount):
    currency_data = {
        'USD': '1',
        'NGN': '411.57',
        'YUA': '6.46',
        'YEN' : '109.47',
	}

    from_curr_value = int(currency_data[from_curr])
    to_curr_value = int(currency_data[to_curr])

    value = (to_curr_value/from_curr_value) * int(amount)

    return value

    