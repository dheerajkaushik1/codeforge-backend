from rest_framework.decorators import api_view
from rest_framework.response import Response
import subprocess
import tempfile
import os

@api_view(['POST'])
def run_code(request):
    code = request.data.get("code")

    if not code:
        return Response({"output": "No code provided ❌"})

    try:
        # Create temp C file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".c") as temp:
            temp.write(code.encode())
            file_name = temp.name

        exe_file = file_name.replace(".c", "")

        # Compile
        compile_process = subprocess.run(
            ["gcc", file_name, "-o", exe_file],
            capture_output=True,
            text=True
        )

        if compile_process.returncode != 0:
            return Response({"output": compile_process.stderr})

        # Run
        input_data = request.data.get("input", "")
        run_process = subprocess.run(
            [exe_file],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=5
        )

        return Response({"output": run_process.stdout})
    
    except Exception as e:
        return Response({"output": f"Server error: {str(e)}"})

    finally:
        try:
            os.remove(file_name)
            os.remove(exe_file)
        except:
            pass
