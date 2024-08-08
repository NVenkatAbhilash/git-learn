
import subprocess

@app.route('/run_command', methods=['GET'])
def run_command():
    # Retrieve the command string from query parameters
    command_str = request.args.get('command')

    if not command_str:
        return jsonify({"error": "The 'command' parameter is required."}), 400

    # Split the command string into command and arguments
    # This assumes that the command and arguments are space-separated
    full_command = command_str.split()

    try:
        # Run the command
        result = subprocess.run(full_command, text=True, capture_output=True, check=True)

        # Return the output and errors
        return jsonify({
            "output": result.stdout,
            "errors": result.stderr
        })

    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": f"Command '{' '.join(full_command)}' failed with exit code {e.returncode}",
            "stderr": e.stderr
        }), 500
