from models import Driver
from parse.factory import Parser
from parse.op import RootOp


user_query = """
age = today - user.birthday
full_name = firstname + ' ' + lastname
is_adult = 18 < age
constant = 2 * 3

first_name == 'ali' or age > 25 and nation == 'Iranian' and male
"""


parser = Parser()
root_op = parser.parse(user_query)
print(RootOp(root_op, Driver).eval())
