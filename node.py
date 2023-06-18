import json
from abc import ABC
from collections import namedtuple

class Node(ABC):
    def toJSON(self):
        pass

def customNodeDecoder(nodeDict):
    return namedtuple('X', nodeDict.keys())(*nodeDict.values())

class NumberNode(Node):
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'

    def toJSON(self):
        json_val = {
            'type': type(self).__name__,
            'tok': self.tok.toJSON()
        }
        return json_val


class StringNode(Node):
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'

    def toJSON(self):
        json_val = {
            'type': type(self).__name__,
            'tok': self.tok.toJSON()
        }
        return json_val


class ListNode(Node):
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end

    def toJSON(self):
        elements = []

        for node in self.element_nodes:
            elements.append(node.toJSON())

        json_val = {
            'type': type(self).__name__,
            'element_nodes': elements,
            'post_start': self.pos_start.toJSON(),
            'pos_end': self.pos_end.toJSON()
        }
        return json_val


class VarAccessNode(Node):
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

    def toJSON(self):
        json_val = {
            'type': type(self).__name__,
            'var_name_tok': self.var_name_tok.toJSON()
        }
        return json_val


class VarAssignNode(Node):
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

    def toJSON(self):
        json_val = {
            'type': type(self).__name__,
            'var_name_tok': self.var_name_tok.toJSON(),
            'value_node': self.value_node.toJSON()
        }
        return json_val


class BinOpNode(Node):
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

    def toJSON(self):
        json_val = {
            'type': type(self).__name__,
            'left_node': self.left_node.toJSON(),
            'op_tok': self.op_tok.toJSON(),
            'right_node': self.right_node.toJSON(),
        }
        return json_val


class UnaryOpNode(Node):
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'

    def toJSON(self):
        json_val = {
            'type': type(self).__name__,
            'op_tok': self.op_tok.toJSON(),
            'node': self.node.toJSON(),
        }
        return json_val


class IfNode(Node):
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(self.cases) - 1])[0].pos_end

    def toJSON(self):

        cases = []
        for condition, expr, should_return_null in self.cases:
            print('case:', condition)

            if isinstance(condition, Node):
                condition_json = condition.toJSON()
            else:

                try:
                    left = condition[0].toJSON()
                except TypeError:
                    left = condition[0]

                try:
                    right = condition[2].toJSON()
                except TypeError:
                    right = condition[2]

                condition_json = {
                    'left': left,
                    'op': condition[1],
                    'right': right
                }

            case_json = {
                'condition': condition_json,
                'expr': expr.toJSON(),
                'should_return_null': should_return_null
            }

            cases.append(case_json)

        else_case = None
        if self.else_case is not None:
            else_json = {
                'expr': self.else_case[0].toJSON(),
                'should_return_null': self.else_case[1]
            }
            else_case = else_json

        json_val = {
            'type': type(self).__name__,
            'cases': cases,
            'else_case': else_case,
        }
        return json_val


class FuncDefNode:
    def __init__(self, var_name_tok, arg_name_toks, body_node, should_auto_return):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node
        self.should_auto_return = should_auto_return

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end

    def toJSON(self):
        arg_name_toks = []
        for tok in self.arg_name_toks:
            arg_name_toks.append(tok.toJSON())

        json_val = {
            'type': type(self).__name__,
            'var_name_tok': self.var_name_tok.toJSON(),
            'arg_name_toks': arg_name_toks,
            'body_node': self.body_node.toJSON(),
            'should_auto_return': self.should_auto_return
        }

        return json_val


class CallNode(Node):
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end

    def toJSON(self):

        arg_nodes = []
        for case in self.arg_nodes:
            arg_nodes.append(case.toJSON())

        json_val = {
            'type': type(self).__name__,
            'node_to_call': self.node_to_call.toJSON(),
            'arg_nodes': arg_nodes,
        }
        return json_val


class ReturnNode(Node):
    def __init__(self, node_to_return, pos_start, pos_end):
        self.node_to_return = node_to_return

        self.pos_start = pos_start
        self.pos_end = pos_end

    def toJSON(self):
        json_val = {
            'type': type(self).__name__,
            'node_to_return': self.node_to_return.toJSON(),
            'pos_start': self.pos_start.toJSON(),
            'pos_end': self.pos_end.toJSON(),
        }
        return json_val
