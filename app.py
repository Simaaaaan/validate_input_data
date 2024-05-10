from flask import Flask, request, render_template
import re

app = Flask(__name__)

@app.route('/')
def form():
  return render_template('input_data.html')

@app.route('/submit_form', methods=['POST'])
def handle_form():
  id_number = request.form.get('id')
  name = request.form.get('name')
  gender = request.form.get('gender')
  email = request.form.get('email')

  # Validate ID number (assuming 台灣ID)
  if len(id_number) != 10:
    return "身分證號碼應該為10碼", 400

  if not id_number[0].isalpha():
    return "身分證號碼第一個字元應該為英文字母", 400

  # Convert the first letter to a corresponding number
  id_number_num = str(10 + ord(id_number[0].upper()) - ord('A')) + id_number[1:]

  # Calculate the sum according to the steps
  step2_sum = 0
  step3_sum = 0
  for i, char in enumerate(id_number_num):
    if i == 0:
      step2_sum += int(char) * 9
    else:
      step3_sum += int(char) * (10 - i)

  total_sum = step2_sum + step3_sum

  # Check if the ID number is valid
  if total_sum % 10 == 0:
    return "身分證號碼驗證成功", 200
  else:
    return "身分證號碼驗證失敗", 400

  # Validate name (assuming it's alphabetic)
  if not re.match(r'^[A-Za-z\s]+$',name):
    return "Invalid name", 400

  # Validate gender
  if gender not in ['Male', 'Female']:
    return "Invalid gender", 400

  # Validate email
  if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
    return "Invalid email", 400

  return "All entries are valid", 200

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
