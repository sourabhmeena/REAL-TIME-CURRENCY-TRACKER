from sanic import Blueprint
from .convert_route import convert
from .currency_list_route import currency_list
from .help_route import help_
from .home_page_route import home_route__

root_group = Blueprint.group(convert, currency_list, help_, home_route__)
