def delete_dot(text: str):
    result = ''
    for i in range(len(text)):
        if text[i] != '.':
            result = result + text[i]
        else:
            result = result + ' '

    return (result)
