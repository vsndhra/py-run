from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import subprocess
import re

app = Flask(__name__)
CORS(app) 

def run_python(code):
    try:
        if re.search(r'(__|exec|sys)', code):
            raise ValueError("Invalid code detected.")
        
        result = subprocess.run(
            ['python3', '-c', code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5,
            check=True  
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

def run_cpp(code):
    try:
        # Compile the C++ code
        compiled_code = subprocess.run(
            ['g++', '-x', 'c++', '-std=c++17', '-o', 'temp_executable', '-'],
            input=code,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10,
            check=True  
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
            check=True  
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

def run_c(code):
    try:
        # Compile the C code
        compiled_code = subprocess.run(
            ['gcc', '-x', 'c', '-std=c17', '-o', 'temp_executable', '-'],
            input=code,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10,
            check=True  
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
            check=True  
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

def run_java(code):
    try:
        # Write the Java code to a Main file
        with open('Main.java', 'w') as f:
            f.write(code)
        
        # Compile the Java code
        compiled_code = subprocess.run(
            ['javac', 'Main.java'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10,
            check=True  
        )
        
        if compiled_code.returncode != 0:
            raise ValueError("Compilation failed:\n" + compiled_code.stderr)
        
        # Run the compiled Java class
        result = subprocess.run(
            ['java', 'Main'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5,
            check=True,
            cwd='.'
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
            subprocess.run(['rm', 'Main.java', 'Main.class'], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            pass

def run_js(code):
    try:
        # Run the JavaScript code
        result = subprocess.run(
            ['node', '-e', code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5,
            check=True 
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form.get('code')
        language = request.form.get('language')
        if code:
            if language == "python":       # Python language
                output, error = run_python(code)
                return jsonify(output=output, error=error)
            elif language == "cpp":        # C++ language
                output, error = run_cpp(code)
                return jsonify(output=output, error=error)
            elif language == "c":          # C language
                output, error = run_c(code)
                return jsonify(output=output, error=error)
            elif language == "java":       # Java language
                output, error = run_java(code)
                return jsonify(output=output, error=error)
            elif language == "javascript": # Javascript language
                output, error = run_js(code)
                return jsonify(output=output, error=error)

    return render_template('index.html',output='Run to view output', error='')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)