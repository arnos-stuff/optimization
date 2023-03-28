import sympy as sp
import json
import sys
import re

from .inputs import console


def parseInputDefinition(indef):
    """Parse the input definition and return a sympy expression.
    
    Input definitions are expected to be of the form:
    
    `variables: ([\w\d\,]+) | constants: ([\w\d\,]+) | expr: (.+)`
    
    The `variables` and `constants` are optional, but if not provided, the expression is assumed to be a function
    and all the variables are assumed to be free.
    
    Examples:
    
    1. `x**2 + y**2` => `variables: x, y | expr: x**2 + y**2`
    2. `f(x, y) = x**2 + y**2` => `variables: x, y | expr: f(x,y) = x**2 + y**2`
    3. `x = 1; t = 2; x**2 + y**2/t` => `variables: x, y, t| expr: x = 1; t = 2; x**2 + y**2/t`
    4. `{"x": 1, "t": 2, "expr": "x**2 + y**2/t"}` => `variables: x, y, t| expr: {"x": 1, "t": 2, "expr": "x**2 + y**2/t"}`
    """
    
    pass


def parseInputExpr(expr):
    """Parse the input expression and return a sympy expression.
    
    Input expressions are expected to be of the form:
    
    1. one liners: `x**2 + y**2`
    2. named functions: `f(x, y) = x**2 + y**2`
    3. multi-step definitions separated by `;`: `x = 1; t = 2; x**2 + y**2/t`
    4. multi-step definitions declared as JSON: `{"x": 1, "t": 2, "expr": "x**2 + y**2/t"}`
    """
    
    pass

def checkValidJSON(expr):
    try:
        json.loads(expr)
        return True
    except json.JSONDecodeError:
        return False

def guessExprType(expr):
    """Guess the type of the input expression.
    
    The 4 types of expressions are:
    
    1. one liners: `x**2 + y**2`
    2. named functions: `f(x, y) = x**2 + y**2`
    3. multi-step definitions separated by `;`: `x = 1; t = 2; x**2 + y**2/t`
    4. multi-step definitions declared as JSON: `{"x": 1, "t": 2, "expr": "x**2 + y**2/t"}`
    """
    if expr.lstrip().startswith("{") and not checkValidJSON(expr):
        console.log("⚠️ [bold red] Invalid JSON expression.[/bold red]")
        sys.exit(1)
    elif expr.lstrip().startswith("{") and checkValidJSON(expr):
        return "json", json.loads(expr)
    elif matches := re.findall(r"(\w+)\(([\w\d\,]+)\)\s*=\s*(.+)", expr):
        varnames = matches[0][1].split(",")
        funcname = matches[0][0]
        parsed_expr = matches[0][2]
        
        return "named", {
            "variables": varnames,
            "function": funcname,
            "expr": parsed_expr
        }
    elif ";" in expr:
        kind = "multi"
        terms = []
        steps = expr.count(";") + 1
        for i,xpr in enumerate(expr.split(";")):
            if not xpr.strip():
                continue
            elif i == steps - 1:
                terms.append({
                    "expr": xpr
                    "step": i
                })
            elif not (matches := re.findall(r"(.+)\s*=\s*(.+)", xpr)):
                console.log("⚠️ [bold red] Invalid multi-step expression.[/bold red]")
                sys.exit(1)
            else:
                terms.append({
                    "variable": matches[0][0],
                    "expr": matches[0][1]
                    "step": i
                })
                
    else:
        console.log("⚠️ [bold red] Invalid expression.[/bold red]")
        sys.exit(1)
            
    return kind, terms
            
    
    
    
    