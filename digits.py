def digits(data: str):
    result = ''
    for i in range(len(data)):
        k = data[i]
        if data[i].isdigit():
            result = result + str(data[i])
    return int(result)
