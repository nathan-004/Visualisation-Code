import ast

python_code = "a = 2\nb = a + 3\nprint(b)\ndef my_function(x):\n    return x * 2\nresult = my_function(5)\nprint(result)"

class PythonSyntaxTree:
    """A simple Python debugger that analyzes the syntax tree of the provided code."""

    def __init__(self, code):
        self.code = code
        self.steps = []

    def analyse_syntax_tree(self):
        """Analyzes the syntax tree and prints the structure."""
        tree = ast.parse(self.code)
        
        self.node_visitor(tree)

        print(self.steps)

    def node_visitor(self, node, return_value=False):
        """
        Visits each node in the syntax tree.
        Implemented :
        - visit_assign: Handles assignment nodes.
        """

        self.return_value = return_value
        attribute_name = f"visit_{type(node).__name__.lower()}"
        method = getattr(self, attribute_name, None)

        if method:
            res = method(node)
            return res

        print(f"Visiting node: {type(node).__name__}")

        for child_node in ast.iter_child_nodes(node):
            self.node_visitor(child_node)

    def visit_assign(self, node):
        """Handles assignment nodes."""
        
        self.steps.append({"type": node.__class__.__name__, "targets": [target.id for target in node.targets], "values": ast.dump(node.value) if isinstance(node.value, ast.Constant) else self.node_visitor(node.value, return_value=True)})

    def visit_call(self, node):
        """Handles function call nodes."""
        
        args = []
        for arg in node.args:
            if isinstance(arg, ast.Str):  # String literal
                args.append(arg.s)
            elif isinstance(arg, ast.Num):  # Numeric literal
                args.append(arg.n)
            elif isinstance(arg, ast.Name):  # Variable
                args.append(arg.id)
            else:
                args.append(ast.dump(arg))  # Fallback for other types

        if not self.return_value:
            self.steps.append({"type": node.__class__.__name__, "function": node.func.id, "args": args})
        else:
            return {"type": node.__class__.__name__, "function": node.func.id, "args": args}     

debugger = PythonSyntaxTree(python_code)
debugger.analyse_syntax_tree()

# https://medium.com/@dev.aguillin/abstract-syntax-tree-python-85d39a53e86d#0c60
