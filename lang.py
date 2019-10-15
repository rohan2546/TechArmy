from subprocess import Popen, PIPE
import time
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
import os
import signal

#   Getting JAVA class name
def get_class_name(program_path):
    fptr = open(program_path+'.txt',"r")
    contents = tuple(fptr)
    fptr.close()

    contents =[x.strip()  for x in contents]

    for lines in contents:
        words = []
        if 'class' in lines:
            words = lines.split(' ')
            for i in range(len(words)):
                if words[i]=='class':
                    return words[i+1]
            break

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
        pid = os.getpid()
        fp = open("problems/"+self.problem_id+"/in"+str(p)+".txt", "r")
        contents = fp.read()
        fp.close()

        def signal_handler(signum, frame):
            raise Exception("Timed out!")

        timeout = False
        #signal.signal(signal.SIGALRM, signal_handler)
        # signal.alarm(self.time_out)   # timeout seconds
        stdout = ''
        stderr = 'e'
        #t = 2
        # try:
        start_time = time.time()
        op = Popen(["timeout", "2s", "python", code_path], stdin=PIPE,
                   stdout=PIPE, stderr=PIPE)
        stdout, stderr = op.communicate(contents.encode("utf-8"))
        t = (time.time() - start_time)
        stdout = stdout.decode()
        stderr = stderr.decode()
        # try:
        #    os.kill(op.pid, signal.SIGKILL)
        # except:
        #    pass
        # except Exception as i:
        #    timeout = True
        #    return(stdout, stderr, t, pid)

        # write code to compare output with test_case_op file and update value of status
        # fp = open("problems/"+self.problem_id+"/op"+str(p)+".txt", "r")
        # contents = fp.read()
        # fp.close()

        # status = (stdout == contents)

        return(stdout, stderr, t, pid)

    def get_number_of_testcases(self):
        fp = open("problems/"+self.problem_id+"/number_cases.txt", "r")
        contents = fp.read()
        return (int(contents))

    def py_lang(self):
        code_path = self.code_path+".py"

        # to check for compilation error; dont proceed into threading if compilation error
        #op = Popen(["python", code_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        #stdout, stderr = op.communicate()
        #stdout = stdout.decode()
        #stderr = stderr.decode()
        stderr = ''
        try:
            os.kill(op.pid, signal.SIGKILL)
        except:
            pass
        if(stderr == ''):
            testcases = self.get_number_of_testcases()
            #p = Pool(processes=testcases)
            p = ThreadPool()
            results = p.map(self.processes_py, list(range(testcases)))
            p.close()
            # for stdout, stderr, t, pid in results:
            #     try:
            #         os.kill(op.pid, signal.SIGKILL)
            #     except:
            #         pass
            # p.terminate()
            # p.join()

            return results, 1

        else:

            return stderr, 0

    def processes_C(self, p):

        fp = open("problems/"+self.problem_id+"/in"+str(p)+".txt", "r")
        contents = fp.read()
        fp.close()

        # def signal_handler(signum, frame):
        #     raise Exception("Timed out!")

        # timeout = False
        # signal.signal(signal.SIGALRM, signal_handler)
        # signal.alarm(self.time_out)   # timeout seconds

        # try:
        start_time = time.time()
        op = Popen(["timeout","2s",self.student_path+"/./a.out"],
                    stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = op.communicate(contents.encode("utf-8"))
        t = (time.time() - start_time)
        stdout = stdout.decode()
        stderr = stderr.decode()

        # except Exception as i:
        #     timeout = True
        #     return(timeout)

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

        if(stderr == ''):
            testcases = self.get_number_of_testcases()

            p = ThreadPool()
            results = p.map(self.processes_C, list(range(testcases)))
            p.close()

            return results, 1

        else:

            return stderr, 0

    def processes_cpp(self, p):

        fp = open("problems/"+self.problem_id+"/in"+str(p)+".txt", "r")
        contents = fp.read()
        fp.close()

        # def signal_handler(signum, frame):
        #     raise Exception("Timed out!")

        # timeout = False
        # signal.signal(signal.SIGALRM, signal_handler)
        # signal.alarm(self.time_out)   # timeout seconds

        # try:
        start_time = time.time()
        op = Popen(["timeout","2s",self.student_path+"/./a.out"],
                    stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = op.communicate(contents.encode("utf-8"))
        t = (time.time() - start_time)
        stdout = stdout.decode()
        stderr = stderr.decode()

        # except Exception as i:
        #     timeout = True
        #     return(timeout)

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

        if(stderr == ''):
            testcases = self.get_number_of_testcases()

            p = ThreadPool()
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

        # try:
        start_time = time.time()
        op = Popen(["timeout","2s","java", self.student_path+"/temp"],
                    stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = op.communicate(contents.encode("utf-8"))
        t = (time.time() - start_time)
        stdout = stdout.decode()
        stderr = stderr.decode()

        # except Exception as i:
        #     timeout = True
        #     return(timeout)

        # write code to compare output with test_case_op file and update value of status
        fp = open("problems/"+self.problem_id+"/op"+str(p)+".txt", "r")
        contents = fp.read()
        fp.close()

        status = (stdout == contents)

        return(stdout, stderr, status, t)

    def java_lang(self):
        new_code_path = get_class_name(self.code_path)
        code_path = new_code_path+".java"

        op = Popen(["javac", code_path],
                   stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = op.communicate()
        stdout = stdout.decode()
        stderr = stderr.decode()

        if(stderr != ''):
            testcases = get_number_of_testcases()

            p = ThreadPool()
            results = p.map(self.processes_java, list(range(testcases)))
            p.close()

            return results, 1

        else:

            return stderr, 0
