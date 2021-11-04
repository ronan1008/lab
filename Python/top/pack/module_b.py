# from module_a import test
from .module_a import test
from ..pack2.module_y import test2
from . import module_a
import sys
print(sys.path)
test()
test2()
module_a.test()
