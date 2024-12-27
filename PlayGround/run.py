import os 

def read_file(file_name):
    with open(file_name,'r') as f:
        content = f.read()
    return content
def write_file(string):
    with open('PlayGround/main.py','w') as f:
        f.write(string)

def play():
    file_to_execute = 'PlayGround/main.py'
    program = read_file(file_to_execute)
    if('input(' in program):
        feedback = {
            'info':"As Program contain input field I am unable to run the program"
        }
        return str(feedback) + " I'll write program without input fuction. Here is your program"
    else:
        os.system(f"python3 {file_to_execute} > PlayGround/output.txt 2>&1 ")
        feedback = {}
        feedback['file_name']='main.py'
        feedback['program_output']=read_file('PlayGround/output.txt')
        files = os.listdir('PlayGround/')
        files.remove('run.py')
        files.remove('output.txt')
        os.system("rm -r PlayGround/output.txt")
        os.system("rm -r PlayGround/main.py")
        feedback['environment_file_list']=files
        return str(feedback)+" According to the environment output"
    
