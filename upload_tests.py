import json
import os
import sys
import codepost
from grade_nb import gradeNotebook

# NOTE: THIS SHOULD BE EDITED BY USER BASED ON DESIRED BEHAVIOR. File name for codePost
# Make sure to install prof Oh's Gofer Grader.
# pip install git+https://github.com/ucsb-pstat/Gofer-Grader.git
# change course ID as needed or maybe make it part of the script.
COURSE_ID = 345


def upload_output(name, code, subID):
    file = codepost.file.create(
        name=name, extension="txt", code=code, submission=subID)
    return file.id


def parse_test_output(test_output):
    """
    Given a test output file and returns the file to be uploaded to codePost
    NOTE: THIS FUNCTION SHOULD BE EDITED BASED ON DESIRED USER BEHAVIOR
    """
    # question_data = test_output.split("Question")
    # output = []
    # for question in enumerate(question_data):
    #     if "k." in question:
    #         output.append("Question " + question[:4] + " failed a test.")

    # example: returns full test output
    return test_output


def add_comments(score_output, code_file):
    """
    Adds comments to a codePost file, given an API Key, output to parse for comments, and a file object
    NOTE: THIS FUNCTION SHOULD BE EDITED BASED ON DESIRED USER BEHAVIOR
    """

    for i, key in enumerate(score_output.keys()):
        if (score_output[key] == 0):
            comment = {
                'file': code_file,
                'text': "Test not passed!",
                'pointDelta': 1,
                'rubricComment': None,
                'startChar': 0,
                'endChar': 1,
                'startLine': i + 1,
                'endLine': i + 1
            }
            codepost.comment.create(**comment)


def getAssignmentData(assignmentName, courseID=COURSE_ID):
    """ Get assignment for given assignemnt name """
    course = codepost.course.retrieve(id=courseID)
    assignment = course.assignments.by_name(assignmentName)
    return assignment


def getSubmission(assignment, studentEmail):
    try:
        sub = assignment.list_submissions(student=studentEmail)[0]
    except:
        sub = codepost.submission.create(
            assignment=assignment.id, students=[studentEmail])
    finally:
        print(sub.id)
    return sub


def processAllNotebooks(output_dir, assignment):
    """ Processes all notebooks in input directory for the assignment name
    and saves them to ouput directory
    """
    for file in os.listdir(output_dir):
        if(file.endswith(".ipynb")):
            try:
                print("Uploading Tests for: " + file + " 🤔")
                filepath = output_dir + '/' + file

                idx = file.rfind("_")
                student_email = file[:idx]
                submission = getSubmission(assignment, student_email)

                r, s = gradeNotebook(filepath)

                nice_r = r['msg'] + "\n Points: " + str(r['total'])

                nice_s = json.dumps(s, indent=4, sort_keys=True)

                upload_output("Results.txt", nice_r, submission.id)
                score_file = upload_output("Score.txt", nice_s, submission.id)

                code_file = submission.files.by_name(
                    name=assignment.name + ".ipynb")

                add_comments(s, score_file)
                print(file + " has Score and Results uploaded! 🎊")
            except Exception as e:
                print("❌!!ERROR!!❌:" + str(e))


def startProcess(output_dir, assignment_name):
    """ Runs all of the processing """
    assignment = getAssignmentData(assignment_name)
    processAllNotebooks(output_dir, assignment)


def checkSysArgs():
    """ Checks to see if the right amount of parameters are passed by command line """
    if len(sys.argv) < 3:
        raise Exception(
            "There are missing parameters. The following are necessary Input Directory, Output Direcory, Assignment Name")


if __name__ == "__main__":
    checkSysArgs()
    output_dir, assignment_name, *rest = sys.argv[1:]
    startProcess(output_dir, assignment_name)
