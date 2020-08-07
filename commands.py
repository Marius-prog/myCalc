def add(n1, n2):
    return float(n1) + float(n2)


def subtract(n1, n2):
    return float(n1) - float(n2)


def multiply(n1, n2):
    return float(n1) * float(n2)


def divide(n1, n2):
    try:
        div = float(n1) / float(n2)
        return div
    except ZeroDivisionError:
        print("Radom dalyba is nulio")
        return "Cannot delete by 0"