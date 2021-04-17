import os
import sys
from datetime import datetime
import importlib.util
import inspect
import random
import string


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def parameterization(func):
    args_needed = inspect.getfullargspec(func).args
    if args_needed[0] == "self":
        args_needed.pop(0)

    para = []
    random.seed(1)
    for arg in args_needed:
        if inspect.signature(func).parameters[arg].default == inspect._empty:
            if inspect.signature(func).parameters[arg].annotation == int:
                para.append(random.randint(0, sys.maxsize))
            elif inspect.signature(func).parameters[arg].annotation == float:
                para.append(random.random())
            elif inspect.signature(func).parameters[arg].annotation == str:
                para.append("".join(random.choice(string.ascii_lowercase) for i in range(10)))
            elif inspect.signature(func).parameters[arg].annotation == bool:
                para.append(random.choice([True, False]))
        else:
            para.append(inspect.signature(func).parameters[arg].default)

    return para


def flushPrintToString(func, para):
    import io
    stdout = sys.stdout
    sio = io.StringIO()
    sys.stdout = sio
    func(*para)
    sys.stdout = stdout
    sio.seek(0)
    return sio.read()


def compilingReport(paras_a, results_a, paras_b, results_b, identifiers, current_time, runtime):
    filename = "test_report_" + current_time + ".txt"
    report = open(filename, "w")
    report.write("======================================================================\n")
    message = "Timestamp: " + current_time + "\n"
    elapsed_time = float(runtime.seconds) + float(runtime.microseconds) / 1e6
    message += "Ran " + str(len(identifiers)) + " tests in " + str(elapsed_time) + "s\n"
    message += "----------------------------------------------------------------------\n"
    report.write(message)
    for idx in range(len(identifiers)):
        if results_a[idx] == results_b[idx]:
            message = identifiers[idx] + "() PASSED\n"
            message += "----------------------------------------------------------------------\n"
            report.write(message)
        else:
            message = identifiers[idx] + "() FAILED\n"
            message += "Test parameters used in version A: " + str(paras_a[idx]) + "\n"
            message += "Test result in version A: \n" + str(results_a[idx]) + "\n"
            message += "Test parameters used in version B: " + str(paras_b[idx]) + "\n"
            message += "Test result in version B: \n" + str(results_b[idx]) + "\n"
            message += "----------------------------------------------------------------------\n"
            report.write(message)
    report.write("======================================================================\n")


def regTest(dir_a, dir_b, code, identifiers):
    print("RegTest starts.")
    start_time = datetime.now()
    current_time = start_time.strftime("%d-%m-%Y_%H:%M:%S")
    print("Timestamp: " + current_time)
    paras_a = []
    results_a = []
    paras_b = []
    results_b = []
    for identifier in identifiers:
        if "." in identifier:   # check whether the identifier passed is a function in the code or a function under a class in the code
            has_class = True
            class_name = identifier.split(".")[0]
            func_name = identifier.split(".")[1]
        else:
            has_class = False
            func_name = identifier

        spec_a = importlib.util.spec_from_file_location(identifier, dir_a + code)
        module_a = importlib.util.module_from_spec(spec_a)
        spec_a.loader.exec_module(module_a)
        if has_class:
            class_a = getattr(module_a, class_name)
            class_a_instance = class_a()
            method_to_call_a = getattr(class_a_instance, func_name)
            para = parameterization(method_to_call_a)
            with HiddenPrints():
                return_values_a = method_to_call_a(*para)
        else:
            method_to_call_a = getattr(module_a, func_name)
            para = parameterization(method_to_call_a)
            with HiddenPrints():
                return_values_a = method_to_call_a(*para)

        if return_values_a is None:
            return_values_a = flushPrintToString(method_to_call_a, para)

        paras_a.append(para)
        results_a.append(return_values_a)

        spec_b = importlib.util.spec_from_file_location(identifier, dir_b + code)
        module_b = importlib.util.module_from_spec(spec_b)
        spec_b.loader.exec_module(module_b)
        if has_class:
            class_b = getattr(module_b, class_name)
            class_b_instance = class_b()
            method_to_call_b = getattr(class_b_instance, func_name)
            para = parameterization(method_to_call_b)
            with HiddenPrints():
                return_values_b = method_to_call_b(*para)
        else:
            method_to_call_b = getattr(module_b, func_name)
            para = parameterization(method_to_call_b)
            with HiddenPrints():
                return_values_b = method_to_call_b(*para)

        if return_values_b is None:
            return_values_b = flushPrintToString(method_to_call_b, para)

        paras_b.append(para)
        results_b.append(return_values_b)

        # DEBUG:
        # assert(return_values_a == return_values_b), identifier

    runtime = datetime.now() - start_time
    compilingReport(paras_a, results_a, paras_b, results_b, identifiers, current_time, runtime)
    elapsed_time = float(runtime.seconds) + float(runtime.microseconds) / 1e6
    print("Ran " + str(len(identifiers)) + " tests in " + str(elapsed_time) + "s")
    print("RegTest completes.")


def main():
    regTest("./sample/classes/original/", "./sample/classes/modified/", "test.py", ["MathTest.check_owner", "MathTest.plus", "MathTest.plusf", "MathTest.minus", "MathTest.minusf", "MathTest.power", "MathTest.giveOne"])


if __name__ == "__main__":
    main()
