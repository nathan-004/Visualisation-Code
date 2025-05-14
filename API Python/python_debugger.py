import ast

class PythonSyntaxTree:
    """A simple Python debugger that analyzes the syntax tree of the provided code."""

    def __init__(self, code):
        self.code = code
        self.steps = []

    def analyse_syntax_tree(self):
        """Analyzes the syntax tree and prints the structure."""
        tree = ast.parse(self.code)
        print(ast.dump(tree, indent=4))
        self.node_visitor(tree)

    def node_visitor(self, node, return_value=False):
        """
        Visits each node in the syntax tree.
        """
        attribute_name = f"visit_{type(node).__name__.lower()}"
        method = getattr(self, attribute_name, None)

        if method:
            return method(node, return_value=return_value)

        for child_node in ast.iter_child_nodes(node):
            self.node_visitor(child_node, return_value=return_value)

    def visit_assign(self, node, return_value=False):
        """Handles assignment nodes."""
        value = self.node_visitor(node.value, return_value=True)
        step = {
            "type": node.__class__.__name__,
            "targets": [target.id for target in node.targets],
            "values": value,
        }
        if not return_value:
            self.steps.append(step)
        else:
            return step

    def visit_call(self, node, return_value=False):
        """Handles function call nodes."""
        args = []
        for arg in node.args:
            if isinstance(arg, ast.Constant):
                args.append(arg.value)
            elif isinstance(arg, ast.Name):
                args.append(arg.id)
            else:
                args.append(self.node_visitor(arg, return_value=True))

        step = {
            "type": node.__class__.__name__,
            "function": node.func.id,
            "args": args,
        }
        if not return_value:
            self.steps.append(step)
        else:
            return step

    def visit_binop(self, node, return_value=False):
        """Handles binary operation nodes."""
        left = self.node_visitor(node.left, return_value=True)
        right = self.node_visitor(node.right, return_value=True)
        step = {
            "type": node.__class__.__name__,
            "operation": type(node.op).__name__,
            "left": left,
            "right": right,
        }
        if not return_value:
            self.steps.append(step)
        else:
            return step

    def visit_constant(self, node, return_value=False):
        """Handles constant nodes."""
        if return_value:
            return node.value
        else:
            self.steps.append({"type": node.__class__.__name__, "value": node.value})

    def visit_name(self, node, return_value=False):
        """Handles variable nodes."""
        if return_value:
            return node.id
        else:
            self.steps.append({"type": node.__class__.__name__, "name": node.id})

    def visit_functiondef(self, node, return_value=False):
        """Handles function definition nodes."""
        args = [arg.arg for arg in node.args.args]
        function_body = [self.node_visitor(n, return_value=True) for n in node.body]

        step = {
            "type": node.__class__.__name__,
            "name": node.name,
            "args": args,
            "body": function_body,
        }
        if return_value:
            return step
        else:
            self.steps.append(step)

    def visit_return(self, node, return_value=False):
        """Handles return nodes."""
        value = self.node_visitor(node.value, return_value=True)
        step = {"type": node.__class__.__name__, "value": value}
        if return_value:
            return step
        else:
            self.steps.append(step)

    def print(self):
        for step in self.steps:
            print(step["type"], step)



class PythonInterpreter:
    """A simple Python interpreter that executes the provided code."""

    def __init__(self, code=None, steps=None):
        if code is None and steps is None:
            raise ValueError("Either code or steps must be provided.")
        elif steps is not None:
            self.steps = steps
        elif code is not None:
            self.code = code
            PST = PythonSyntaxTree(code)
            PST.analyse_syntax_tree()
            self.steps = PST.steps

        self.env = {} # Environment to store variables and their values
        self.values_visualization = [] # List to store values for visualization over time

    def execute(self):
        """Executes the code step by step and stores the results in self.env and self.values_visualization."""
        
        for step in self.steps:
            atr = f"execute_{step['type'].lower()}" # Nom de la fonction

            method = getattr(self, atr, None)

            if method:
                method(step)


    def execute_assign(self, step):
        pass

python_code = """
a= 2
b = a + 3
print(b)
def my_function(x):
    return x * 2
result = my_function(5)
print(result)
"""

PST = PythonSyntaxTree(python_code) # Constant
PST.analyse_syntax_tree()
PST.print()
print()
PI = PythonInterpreter(steps=PST.steps)
PI.execute()

# https://medium.com/@dev.aguillin/abstract-syntax-tree-python-85d39a53e86d#0c60
