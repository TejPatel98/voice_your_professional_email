'''
This is the main program that integrates all of the components.
'''
from voice_interperet import collect_speech
#from emailBot import get_response
import sys
import random
from http.server import HTTPServer, BaseHTTPRequestHandler


instruction_queue = []
result_dict = {}
current_instruction = ""

class BoilermakeHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(s):
        '''
        The GET method will fetch the latest instruction from the instruction queue
        and place it in the "processing" queue. The POST method will handle the user's response
        to that particular instruction.
        '''
        # Global variables! Don't try this at home (a.k.a. outside a hackathon), kids!
        global instruction_queue
        global result_dict
        global current_instruction

        print('Received GET request')

        s.send_response(200)
        s.send_header('Content-type', 'text/html')
        s.end_headers()

        if (len(instruction_queue) > 0):
            first_instruction = instruction_queue[0]
            current_instruction = first_instruction[1]
            instruction_queue.remove(first_instruction)

            s.wfile.write(first_instruction[0].encode())
        else:
            if (current_instruction != ""):
                current_instruction = ""
                s.wfile.write(b'Done! What else do you need?')
            else:
                s.wfile.write(b'I didn\'t quite get that.')

    def do_POST(s):
        '''
        The POST method will collect input from the user. If there is an instruction in the queue,
        this will store the user's response to the instruction in the result dictionary.
        If there is no instruction, then this function will determine which set of instructions to apply
        based on it.
        '''

        # Global variables! Don't try this at home (a.k.a. outside a hackathon), kids!
        global instruction_queue
        global result_dict
        global current_instruction

        print('Received POST request')

        to_return = 'Unknown instruction'

        if (current_instruction == ""):
            user_input = get_mic_input(debug=False)

            if (user_input.lower() == 'i need help writing a professional email'):
                instruction_queue = [['Sure. What\'s your name?', 'name'], ['Got it. What is your professor\'s name?', 'professor_name'],
                    ['Got it. What is your major?', 'major'], ['Got it. What year are you?', 'grade'], ['Got it. What are some of your interests?', 'interests']]
            to_return = user_input
        else:
            user_input = get_mic_input(debug=False)
            result_dict[current_instruction] = user_input
            to_return = user_input

            # If the instruction queue is empty, go ahead and build the result string
            if (len(instruction_queue) == 0):
                template = open('./templates/professor_email.txt')
                template_text = template.read().format(**result_dict)

                # Create lists of each possible combo of emails
                email_combos = [[]]
                for line in template_text.split('\n'):
                    if line == '':
                        email_combos.append([])
                    else:
                        email_combos[len(email_combos)-1].append(line)

                # Choose which lines we want to use
                final_result = ""
                for combos in email_combos:
                    if (len(combos) > 1):
                        final_result += combos[random.randint(0, len(combos)-1)] + '\n'
                    else:
                        final_result += combos[0] + '\n'
                result_file = open('./output/professor_email.txt', 'w')
                result_file.write(final_result)

        s.send_response(200)
        s.send_header('Content-type', 'text/html')
        s.end_headers()
        s.wfile.write(to_return.encode())

def get_mic_input(debug=True):
    if (debug):
        return sys.stdin.readline()[:-1].lower()
    else:
        return collect_speech()

def professoinal_email_prompt(debug=True):
    to_return = {}
    print('Got it. What is your name?')
    to_return['student_name'] = get_mic_input(debug=debug)
    print('Got it. What is your professor\'s name?')
    to_return['professor_name'] = get_mic_input(debug=debug)
    print('Got it. What is the name of the course?')
    to_return['course_name'] = get_mic_input(debug=debug)
    print('Got it. I am writing the email now.')
    template = open('./templates/email.txt')
    template_text = template.read().format(**to_return)
    return template_text

def main(debug=True):
    print('Welcome! How can I help?')
    bot_response = ""
    while (bot_response != "Bye"):
        user_response = get_mic_input(debug=debug)
        if (user_response == 'bye'):
            print('Bye')
            return
        else:
            if (user_response == 'i need help writing a professional email'):
                print(professoinal_email_prompt(debug=debug))

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, BoilermakeHTTPRequestHandler)
    httpd.serve_forever()