from rest_framework.pagination import PageNumberPagination

base_url = "http://localhost:8000/"


def response_formatter(result, status, message):
    context = {
        'status': status,
        'message': message,
        'result': result
    }

    return context


def send_sms(self, message, mobail):
    pass


def generate_code(number: int):
    from random import randint
    number = int(number)
    return randint(10 ** (number - 1), 10 ** (number))


class CustomPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


def format_currency(value):
    return "{:,.0f}".format(value) + 'تومان'
