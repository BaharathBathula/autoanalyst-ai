import re
import io
import contextlib
import matplotlib.pyplot as plt


def extract_python_code(gemini_text: str) -> str:
    # Try fenced block
    m = re.search(r"```python\s*(.*?)```", gemini_text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()

    # Fallback: everything after PYTHON_CODE:
    m2 = re.search(r"PYTHON_CODE:\s*(.*)", gemini_text, re.DOTALL | re.IGNORECASE)
    if m2:
        return m2.group(1).strip()

    # Last fallback: return full text (sometimes model outputs plain code)
    return gemini_text.strip()


def run_user_code(code: str, df):
    # Reset any previous figures
    plt.close("all")

    # ✅ allow import statements (needed because generated code often imports libs)
    safe_globals = {
        "__builtins__": {
            "__import__": __import__,

            # common safe builtins
            "print": print,
            "len": len,
            "range": range,
            "min": min,
            "max": max,
            "sum": sum,
            "abs": abs,
            "round": round,

            "list": list,
            "dict": dict,
            "set": set,
            "tuple": tuple,
            "sorted": sorted,
            "enumerate": enumerate,
            "zip": zip,

            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
        }
    }

    # Locals provided to the generated code
    safe_locals = {"df": df, "plt": plt}

    stdout_buf = io.StringIO()
    with contextlib.redirect_stdout(stdout_buf):
        exec(code, safe_globals, safe_locals)

    # Collect charts as PNG BYTES (prevents Streamlit/browser caching issues)
    charts = []
    for fignum in plt.get_fignums():
        fig = plt.figure(fignum)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
        buf.seek(0)

        charts.append(buf.getvalue())
        plt.close(fig)

    # Close everything cleanly
    plt.close("all")

    if not charts:
        stdout_buf.write("\n[NOTE] No matplotlib figures were created by the generated code.\n")

    return stdout_buf.getvalue(), charts