import ast
from django.db.models import Q, Model


class BaseOp:
    node: ast.AST

    def __init__(self, node) -> None:
        self.node = node
        self.validate()

    def eval(self):
        raise NotImplementedError

    def validate(self):
        pass


class RootOp(BaseOp):
    node: ast.Module
    model: Model

    def __init__(self, node, model):
        self.node = node
        self.model = model
        self.validate()

    def validate(self):
        # but it's not necessary !
        # nodes = self.node.body
        # self.expr = self.node.body[-1]
        # assert isinstance(self.expr, ast.Expr), "only last item can be filter expression"
        # self.aliases = list(filter(lambda expression: isinstance(expression, ast.Assign), nodes))
        # assert len(self.aliases) + 1 == len(
        #     nodes
        # ), "only one filter expression is allowed and only filter and alias expression are allowed"
        valid_ops = [ast.Assign, ast.Expr]
        invalid_ops = list(filter(lambda op: op in valid_ops, self.node.body))
        assert len(invalid_ops) == 0, invalid_ops

    def eval(self):
        queryset = self.get_queryset()
        ops = self.get_operations()
        for op in ops:
            if isinstance(op, ast.Expr):
                queryset = queryset.filter(FilterOp(op).eval())
            elif isinstance(op, ast.Assign):
                queryset = queryset.alias(AliasOp(op).eval())

    def get_queryset(self):
        return self.model.objects.all()

    def get_operations(self):
        return self.node.body


class AliasOp(BaseOp):
    def eval(self):
        print(self.node)
        return

    def validate(self):
        assert isinstance(self.node, ast.Assign)


class FilterOp(BaseOp):
    node: ast.Expr

    def eval(self):
        if isinstance(self.node, ast.Expr):
            return Expr(self.node).eval()
        elif isinstance(self.node, ast.BoolOp):
            return BoolOp(self.node).eval()
        elif isinstance(self.node, ast.Compare):
            return Compare(self.node).eval()

    def validate(self):
        pass


class Expr(BaseOp):
    node: ast.Expr

    def eval(self):
        return FilterOp(self.node.value).eval()


class BoolOp(BaseOp):
    node: ast.BoolOp

    def eval(self):
        if isinstance(self.node.op, ast.Or):
            return Or(self.node).eval()
        elif isinstance(self.node.op, ast.And):
            return And(self.node).eval()


class Or(BaseOp):
    node: ast.Or

    def eval(self):
        return Q(FilterOp(self.node.values[0]).eval()) | Q(FilterOp(self.node.values[1]).eval())


class And(BaseOp):
    node: ast.Or

    def eval(self):
        return Q(FilterOp(self.node.values[0])) & Q(FilterOp(self.node.values[1]))


class Compare(BaseOp):
    def eval(self):

        for i, (op, comp) in enumerate(zip(self.node.ops, self.node.comparators)):
            if isinstance(op, ast.Eq):
                return Eq(self.node).eval(i)
        return Q()


class Eq(BaseOp):
    def eval(self, i):
        return Q(**{self.node.left.id: self.node.comparators[i].value})
