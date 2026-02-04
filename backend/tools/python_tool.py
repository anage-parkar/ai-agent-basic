import io
import sys
import base64
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from typing import Dict, Any, Optional
import traceback


class PythonTool:
    """Execute Python code in a restricted environment"""
    
    ALLOWED_IMPORTS = {
        'pandas', 'numpy', 'matplotlib', 'seaborn', 'datetime', 
        'math', 'statistics', 'json', 'collections', 're'
    }
    
    def __init__(self):
        self.name = "python"
        self.description = """Execute Python code for data analysis.
Allowed libraries: pandas, numpy, matplotlib, seaborn, datetime, math, statistics, json, collections, re
Returns: Text output and any matplotlib plots as base64 images
Input format: {"code": "your python code here"}"""
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Python code and capture output"""
        code = input_data.get("code", "")
        
        if not code:
            return {"error": "No code provided"}
        
        # Check for dangerous operations
        dangerous_keywords = ['import os', 'import sys', 'import subprocess', 
                             '__import__', 'eval(', 'exec(', 'open(', 'file(']
        for keyword in dangerous_keywords:
            if keyword in code.lower():
                return {"error": f"Forbidden operation: {keyword}"}
        
        # Prepare execution environment
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        redirected_output = io.StringIO()
        redirected_error = io.StringIO()
        
        # Allowed globals
        safe_globals = {
            '__builtins__': __builtins__,
            'print': print,
        }
        
        # Import allowed modules
        try:
            import pandas as pd
            import numpy as np
            import matplotlib.pyplot as plt
            import seaborn as sns
            from datetime import datetime, timedelta
            import math
            import statistics
            import json
            import collections
            import re
            
            safe_globals.update({
                'pd': pd,
                'np': np,
                'plt': plt,
                'sns': sns,
                'datetime': datetime,
                'timedelta': timedelta,
                'math': math,
                'statistics': statistics,
                'json': json,
                'collections': collections,
                're': re,
            })
        except ImportError as e:
            return {"error": f"Import error: {str(e)}"}
        
        try:
            # Redirect stdout/stderr
            sys.stdout = redirected_output
            sys.stderr = redirected_error
            
            # Execute code
            exec(code, safe_globals)
            
            # Capture text output
            output = redirected_output.getvalue()
            error_output = redirected_error.getvalue()
            
            # Capture matplotlib figures
            images = []
            figures = plt.get_fignums()
            for fig_num in figures:
                fig = plt.figure(fig_num)
                buf = io.BytesIO()
                fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
                buf.seek(0)
                img_base64 = base64.b64encode(buf.read()).decode('utf-8')
                images.append(img_base64)
                plt.close(fig)
            
            result = {
                "success": True,
                "output": output,
                "images": images
            }
            
            if error_output:
                result["warnings"] = error_output
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"{type(e).__name__}: {str(e)}",
                "traceback": traceback.format_exc()
            }
        
        finally:
            # Restore stdout/stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            plt.close('all')


# Global instance
python_tool = PythonTool()
