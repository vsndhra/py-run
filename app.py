from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import subprocess
import re

app = Flask(__name__)
CORS(app) 

def execute_code_safely(code):
    try:
        # Validate code to prevent malicious code injection
        if re.search(r'(__|exec|sys)', code):
            raise ValueError("Invalid code detected.")
        
        result = subprocess.run(
            ['python3', '-c', code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5,
            check=True  # Raise exception on non-zero exit code
        )
        
        output = result.stdout.strip()
        error = result.stderr.strip()
        
        return output, error
    
    except subprocess.CalledProcessError as e:
        return "", "Code execution failed."
    except subprocess.TimeoutExpired:
        return "", "Execution timed out."
    except Exception as e:
        return "", str(e)

def run_cpp_code(code):
    try:
        # Compile the C++ code
        compiled_code = subprocess.run(
            ['g++', '-x', 'c++', '-std=c++17', '-o', 'temp_executable', '-'],
            input=code,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10,
            check=True  # Raise exception on non-zero exit code
        )
        
        if compiled_code.returncode != 0:
            raise ValueError("Compilation failed.")
        
        # Run the compiled executable
        result = subprocess.run(
            ['./temp_executable'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5,
            check=True  # Raise exception on non-zero exit code
        )
        
        output = result.stdout.strip()
        error = result.stderr.strip()
        
        return output, error
    
    except subprocess.CalledProcessError as e:
        return "", "Code execution failed."
    except subprocess.TimeoutExpired:
        return "", "Execution timed out."
    except Exception as e:
        return "", str(e)
    finally:
        try:
            subprocess.run(['rm', 'temp_executable'], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            pass

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form.get('code')
        language = request.form.get('language')
        if code:
            if language == "python":
                output, error = execute_code_safely(code)
                return jsonify(output=output, error=error)
            elif language == "cpp":
                output, error = run_cpp_code(code)
                return jsonify(output=output, error=error)

    return render_template('index.html', code='',output='Run to view output', error='')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)