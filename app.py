from multiprocessing.pool import ThreadPool
from lang import languages
from flask import Flask, jsonify, request
import os
from subprocess import run, PIPE, check_output
import time
from subprocess import Popen, PIPE
import time
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
import os
import signal
app = Flask(__name__)


def threading(p):
    fp = open("in0"+str(p)+".txt", "r")
    contents = fp.read()
    fp.close()

    import signal

    def signal_handler(signum, frame):
        raise Exception("Timed out!")

    timeout = False
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(2)   # timeout seconds
    try:
        start_time = time.time()
        op = Popen(["python", "temp.py"], stdin=PIPE,
                   stdout=PIPE, stderr=PIPE)
        stdout, stderr = op.communicate(contents.encode("utf-8"))
        t = (time.time() - start_time)
        stdout = stdout.decode()
        stderr = stderr.decode()
    except Exception as i:
        print(i.args[0])
        timeout = True
        return(timeout)

    return(stdout, stderr, t, timeout)
    # write code to compare output with test_case_op file and update value of status


@app.route('/v1/run_code', methods=['POST'])
def compile():
    # recieve contest_id
    # problem_id recieved, populate problem id by making a call to db if folder doesnt exist
    print(request)
    # code = ("print(\"hello\")")
    # language = "py"
    try:
        # make dir for each student under each contest
        os.makedirs(request.json['contest_id'] +
                    "/temp_"+request.json['student_id'])
    finally:

        # store the given code into the student folder
        fp = open(request.json['contest_id']+"/temp_" +
                  request.json['student_id']+"/temp."+request.json['language'], "w")
        fp.write(request.json['code'])
        fp.close()

        # call languages class and get status(coorect/wrong answer) or if error occured
        lang = languages(
            request.json['student_id'], request.json['problem_id'], request.json['contest_id'])
        ip_lang = request.json['language']
        if(ip_lang == "py"):
            status, err = lang.py_lang()
        elif(ip_lang == "c"):
            status, err = lang.C_lang()
        elif(ip_lang == "cpp"):
            status, err = lang.Cpp_lang()
        elif(ip_lang == "java"):
            status, err = lang.java_lang()

    # new_gui = subprocess.Popen(["python", path])
    # keyboard_output = subprocess.check_output(["./a.out <", path[:1],path[2:]]).decode("utf-8")
    # print(keyboard_output)
    # keyboard_output = keyboard_output[:-1]
    # keyboard_output.decode("utf-8")
    # print(keyboard_output)

    # questions = obj.extract_questions(request.json)
    # # {'questions':obj.test_transcript(request.json['transcript'])}

    return jsonify(results), 200


@app.route('/v1/test', methods=['POST'])
def compile_test():
    # recieve contest_id
    # problem_id recieved, populate problem id by making a call to db if folder doesnt exist
    print(request)
    # code = ("print(\"hello\")")
    # language = "py"

    # store the given code into the student folder
    fp = open("temp."+request.json['language'], "w")
    fp.write(request.json['code'])
    fp.close()

    p = Pool(processes=5)
    results = p.map(threading, list(range(5)))
    p.close()

    # keyboard_output = keyboard_output[:-1]
    # keyboard_output.decode("utf-8")
    # print(keyboard_output)

    # questions = obj.extract_questions(request.json)
    # # {'questions':obj.test_transcript(request.json['transcript'])}

    return jsonify(results), 200


if __name__ == '__main__':

    app.run("0.0.0.0", port=5001)
