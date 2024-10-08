from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
import subprocess
import json
import threading
import os
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///macros.db'
db = SQLAlchemy(app)

class Macro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

def escape_adb_text(text):
    special_chars = "|\"'<>;?`&*()~"
    for char in special_chars:
        if char == '&':
            text = text.replace(char, "\\\\\\&")
        elif char == '"':
            text = text.replace(char, '\\"')
        else:
            text = text.replace(char, "\\\\" + char)
    return text.replace(" ", "%s")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_macro', methods=['POST'])
def add_macro():
    data = request.json
    new_macro = Macro(name=data['name'], content=json.dumps(data['content']))
    db.session.add(new_macro)
    db.session.commit()
    return jsonify({"success": True, "id": new_macro.id})

@app.route('/get_macros')
def get_macros():
    macros = Macro.query.all()
    return jsonify([{"id": m.id, "name": m.name, "content": json.loads(m.content)} for m in macros])

@app.route('/update_macro', methods=['POST'])
def update_macro():
    data = request.json
    macro = Macro.query.get(data['id'])
    macro.name = data['name']
    macro.content = json.dumps(data['content'])
    db.session.commit()
    return jsonify({"success": True})

@app.route('/delete_macro', methods=['POST'])
def delete_macro():
    macro_id = request.json['id']
    macro = Macro.query.get(macro_id)
    db.session.delete(macro)
    db.session.commit()
    return jsonify({"success": True})

def validate_swipe_params(step):
    required_params = ['x1', 'y1', 'x2', 'y2']
    for param in required_params:
        try:
            step[param] = float(step[param])
        except (ValueError, TypeError):
            raise ValueError(f"Invalid {param} value")
    step['duration'] = int(step.get('duration', 300))
    return True

@app.route('/send_macro', methods=['POST'])
def send_macro():
    data = request.json
    macro = Macro.query.get(data['id'])
    device = data['device']
    content = json.loads(macro.content)
    
    try:
        for step in content:
            if step['type'] == 'text':
                escaped_text = escape_adb_text(step["value"])
                command = f'adb -s {device} shell input text "{escaped_text}"'
                subprocess.run(command, shell=True, check=True)
            elif step['type'] == 'tab':
                command = f'adb -s {device} shell input keyevent 61'
                subprocess.run(command, shell=True, check=True)
            elif step['type'] == 'enter':
                command = f'adb -s {device} shell input keyevent 66'
                subprocess.run(command, shell=True, check=True)
            elif step['type'] == 'wait':
                time.sleep(float(step["value"]))
            elif step['type'] == 'command':
                command = step['value']
                subprocess.Popen(command, shell=True)
            elif step['type'] == 'tap':
                x = step['x']
                y = step['y']
                command = f'adb -s {device} shell input tap {x} {y}'
                subprocess.run(command, shell=True, check=True)
            elif step['type'] == 'swipe':
                validate_swipe_params(step)
                x1, y1, x2, y2 = step['x1'], step['y1'], step['x2'], step['y2']
                duration = step.get('duration', 300)
                command = f'adb -s {device} shell input swipe {x1} {y1} {x2} {y2} {duration}'
                subprocess.run(command, shell=True, check=True)
            # Newly added key events
            elif step['type'] == 'back':
                command = f'adb -s {device} shell input keyevent 4'  # Back button
                subprocess.run(command, shell=True, check=True)
            elif step['type'] == 'home':
                command = f'adb -s {device} shell input keyevent 3'  # Home button
                subprocess.run(command, shell=True, check=True)
            elif step['type'] == 'overview':
                command = f'adb -s {device} shell input keyevent 187'  # Overview/Recent apps
                subprocess.run(command, shell=True, check=True)
            elif step['type'] == 'volume_up':
                command = f'adb -s {device} shell input keyevent 24'  # Volume up
                subprocess.run(command, shell=True, check=True)
            elif step['type'] == 'volume_down':
                command = f'adb -s {device} shell input keyevent 25'  # Volume down
                subprocess.run(command, shell=True, check=True)
            elif step['type'] == 'power':
                command = f'adb -s {device} shell input keyevent 26'  # Power button
                subprocess.run(command, shell=True, check=True)
            else:
                continue
            print("Executed step:", step)
        return jsonify({"success": True})
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": str(e)}), 500
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    

@app.route('/test_step', methods=['POST'])
def test_step():
    data = request.json
    step = data['step']
    device = data['device']

    try:
        if step['type'] == 'text':
            escaped_text = escape_adb_text(step["value"])
            command = f'adb -s {device} shell input text "{escaped_text}"'
            subprocess.run(command, shell=True, check=True)
        elif step['type'] == 'tab':
            command = f'adb -s {device} shell input keyevent 61'
            subprocess.run(command, shell=True, check=True)
        elif step['type'] == 'enter':
            command = f'adb -s {device} shell input keyevent 66'
            subprocess.run(command, shell=True, check=True)
        elif step['type'] == 'wait':
            time.sleep(float(step["value"]))
        elif step['type'] == 'command':
            command = step['value']
            subprocess.Popen(command, shell=True)
        elif step['type'] == 'tap':
            x = step['x']
            y = step['y']
            command = f'adb -s {device} shell input tap {x} {y}'
            subprocess.run(command, shell=True, check=True)
        elif step['type'] == 'swipe':
            validate_swipe_params(step)
            x1, y1, x2, y2 = step['x1'], step['y1'], step['x2'], step['y2']
            duration = step.get('duration', 300)
            command = f'adb -s {device} shell input swipe {x1} {y1} {x2} {y2} {duration}'
            subprocess.run(command, shell=True, check=True)
        # Test for newly added key events
        elif step['type'] == 'back':
            command = f'adb -s {device} shell input keyevent 4'
            subprocess.run(command, shell=True, check=True)
        elif step['type'] == 'home':
            command = f'adb -s {device} shell input keyevent 3'
            subprocess.run(command, shell=True, check=True)
        elif step['type'] == 'overview':
            command = f'adb -s {device} shell input keyevent 187'
            subprocess.run(command, shell=True, check=True)
        elif step['type'] == 'volume_up':
            command = f'adb -s {device} shell input keyevent 24'
            subprocess.run(command, shell=True, check=True)
        elif step['type'] == 'volume_down':
            command = f'adb -s {device} shell input keyevent 25'
            subprocess.run(command, shell=True, check=True)
        elif step['type'] == 'power':
            command = f'adb -s {device} shell input keyevent 26'
            subprocess.run(command, shell=True, check=True)
        else:
            return jsonify({"success": False, "error": "Invalid step type"}), 400

        return jsonify({"success": True})
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": str(e)}), 500
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/get_devices')
def get_devices():
    devices = subprocess.check_output(['adb', 'devices']).decode('utf-8').strip().split('\n')[1:]
    return jsonify([device.split('\t')[0] for device in devices if device and 'device' in device])

@app.route('/screenshot')
def screenshot():
    device = request.args.get('device')
    if not device:
        return 'No device specified', 400

    screenshot_filename = f'screenshot_{device}.png'

    try:
        subprocess.run(f'adb -s {device} shell screencap -p /sdcard/{screenshot_filename}', shell=True, check=True)
        subprocess.run(f'adb -s {device} pull /sdcard/{screenshot_filename} .', shell=True, check=True)
        subprocess.run(f'adb -s {device} shell rm /sdcard/{screenshot_filename}', shell=True, check=True)
        return send_file(screenshot_filename, mimetype='image/png')
    except subprocess.CalledProcessError as e:
        return 'Error taking screenshot: ' + str(e), 500
    finally:
        if os.path.exists(screenshot_filename):
            os.remove(screenshot_filename)

if __name__ == '__main__':
    app.run(debug=True)
