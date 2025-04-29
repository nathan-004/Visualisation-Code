import ast

python_code = "a = 2\nb = a + 3\nprint(b)\ndef my_function(x):\n    return x * 2\nresult = my_function(5)\nprint(result)"

class PythonDebugger:

    def __init__(self, code):
        self.code = code

    def execute_code(self):
        """"Executes the provided Python code and returns the values at each step sous """

        tree = ast.parse(self.code)

        print(ast.dump(tree, indent=4))

debugger = PythonDebugger(python_code)
debugger.execute_code()
