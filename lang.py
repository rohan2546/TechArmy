from subprocess import Popen, PIPE
import time
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
import os
import signal


class languages:

    def __init__(self, student_id, problem_id, contest_id, time_out):
        self.student_id = student_id
        self.problem_id = problem_id
        self.contest_id = contest_id
        self.student_path = contest_id+"/temp_"+student_id
        self.code_path = self.student_path+"/temp"
        self.time_out = time_out

    def processes_py(self, p):
        code_path = self.code_path+".py"

        fp = open("problems/"+self.problem_id+"/in"+str(p)+".txt", "r")
        contents = fp.read()
        fp.close()

        def signal_handler(signum, frame):
            raise Exception("Timed out!")

        timeout = False
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(self.time_out)   # timeout seconds

        try:
            start_time = time.time()
            op = Popen(["python", code_path], stdin=PIPE,
                       stdout=PIPE, stderr=PIPE)
            stdout, stderr = op.communicate(contents.encode("utf-8"))
            t = (time.time() - start_time)
            stdout = stdout.decode()
            stderr = stderr.decode()

        except Exception as i:
            timeout = True
            return(timeout)

        # write code to compare output with test_case_op file and update value of status
        fp = open("problems/"+self.problem_id+"/op"+str(p)+".txt", "r")
        contents = fp.read()
        fp.close()

        status = (stdout == contents)

        return(stdout, stderr, status, t)

    def get_number_of_testcases(self):
        fp = open("problems/"+self.problem_id+"/number_cases.txt", "r")
        contents = fp.read()
        return (int(contents))

    def py_lang(self):
        code_path = self.code_path+".py"

        # to check for compilation error; dont proceed into threading if compilation error
        op = Popen(["python", code_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = op.communicate()
        stdout = stdout.decode()
        stderr = stderr.decode()

        if(stderr != ''):
            testcases = self.get_number_of_testcases()
            p = Pool(processes=testcases)
            results = p.map(self.processes_py, list(range(testcases)))
            p.close()

            return results, 1

        else:

            return stderr, 0

    def processes_C(self, p):

        fp = open("problems/"+self.problem_id+"/in"+str(p)+".txt", "r")
        contents = fp.read()
        fp.close()

        def signal_handler(signum, frame):
            raise Exception("Timed out!")

        timeout = False
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(self.time_out)   # timeout seconds

        try:
            start_time = time.time()
            op = Popen([self.student_path+"/./a.out"],
                       stdin=PIPE, stdout=PIPE, stderr=PIPE)
            stdout, stderr = op.communicate(contents.encode("utf-8"))
            t = (time.time() - start_time)
            stdout = stdout.decode()
            stderr = stderr.decode()

        except Exception as i:
            timeout = True
            return(timeout)

        # write code to compare output with test_case_op file and update value of status
        fp = open("problems/"+self.problem_id+"/op"+str(p)+".txt", "r")
        contents = fp.read()
        fp.close()

        status = (stdout == contents)

        return(stdout, stderr, status, t)

    def C_lang(self):
        code_path = self.code_path+".c"

        def get_number_of_testcases():
            fp = open("problems/"+self.problem_id+"/number_cases.txt", "r")
            contents = fp.read()
            return (int(contents))

        op = Popen(["gcc", "-w", code_path],
                   stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = op.communicate()
        stdout = stdout.decode()
        stderr = stderr.decode()

        if(stderr != ''):
            testcases = self.get_number_of_testcases()

            p = Pool(processes=testcases)
            results = p.map(self.processes_C, list(range(testcases)))
            p.close()

            return results, 1

        else:

            return stderr, 0

    def processes_cpp(self, p):

        fp = open("problems/"+self.problem_id+"/in"+str(p)+".txt", "r")
        contents = fp.read()
        fp.close()

        def signal_handler(signum, frame):
            raise Exception("Timed out!")

        timeout = False
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(self.time_out)   # timeout seconds

        try:
            start_time = time.time()
            op = Popen([self.student_path+"/./a.out"],
                       stdin=PIPE, stdout=PIPE, stderr=PIPE)
            stdout, stderr = op.communicate(contents.encode("utf-8"))
            t = (time.time() - start_time)
            stdout = stdout.decode()
            stderr = stderr.decode()

        except Exception as i:
            timeout = True
            return(timeout)

        # write code to compare output with test_case_op file and update value of status
        fp = open("problems/"+self.problem_id+"/op"+str(p)+".txt", "r")
        contents = fp.read()
        fp.close()

        status = (stdout == contents)

        return(stdout, stderr, status, t)

    def Cpp_lang(self):
        code_path = self.code_path+".cpp"

        op = Popen(["g++", "-w", code_path],
                   stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = op.communicate()
        stdout = stdout.decode()
        stderr = stderr.decode()

        if(stderr != ''):
            testcases = self.get_number_of_testcases()

            p = Pool(processes=testcases)
            results = p.map(self.processes_cpp, list(range(testcases)))
            p.close()

            return results, 1

        else:

            return stderr, 0

    def processes_java(self, p):

        fp = open("problems/"+self.problem_id+"/in"+str(p)+".txt", "r")
        contents = fp.read()
        fp.close()

        def signal_handler(signum, frame):
            raise Exception("Timed out!")

        timeout = False
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(self.time_out)   # timeout seconds

        try:
            start_time = time.time()
            op = Popen(["java", self.student_path+"/temp"],
                       stdin=PIPE, stdout=PIPE, stderr=PIPE)
            stdout, stderr = op.communicate(contents.encode("utf-8"))
            t = (time.time() - start_time)
            stdout = stdout.decode()
            stderr = stderr.decode()

        except Exception as i:
            timeout = True
            return(timeout)

        # write code to compare output with test_case_op file and update value of status
        fp = open("problems/"+self.problem_id+"/op"+str(p)+".txt", "r")
        contents = fp.read()
        fp.close()

        status = (stdout == contents)

        return(stdout, stderr, status, t)

    def java_lang(self):
        code_path = self.code_path+".java"

        op = Popen(["javac", code_path],
                   stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = op.communicate()
        stdout = stdout.decode()
        stderr = stderr.decode()

        if(stderr != ''):
            testcases = get_number_of_testcases()

            p = Pool(processes=testcases)
            results = p.map(self.processes_java, list(range(testcases)))
            p.close()

            return results, 1

        else:

            return stderr, 0
