import markdown


#Insert your student ID here
student_id="0123456789"




md = markdown.Markdown(extensions=['fenced_code'])

input_filename = 'coursework.md'
output_filename = f'5062CEM_2021_22_SepJan_CW1_main_sit_{student_id}.html'

with open(input_filename, 'r') as f:
    html_text = md.convert(f.read())#, output_format='html4')

with open(output_filename, "w") as f:
    f.write(html_text)
