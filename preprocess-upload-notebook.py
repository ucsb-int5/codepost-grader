from shutil import copyfile, copytree, rmtree
import os
import sys
import json
import codepost

COURSE_ID = 345

def readNotebook(nb_path):
    with open(nb_path, 'r') as nb:
        nb_json = nb.read()
    return nb_json


def uploadCode(code, student_email, assignment):
    print(student_email)
    print(assignment.id)
    print(assignment.name)
    try:
        # If submission already exists
        subID = assignment.list_submissions(student=student_email)[0].id
    except:
        # Submission doesn't exist
        subID = codepost.submission.create(
            assignment=assignment.id, students=[student_email]).id
    finally:
        cp_file = codepost.file.create(
            name=assignment.name + ".ipynb", extension="ipynb", code=code, submission=subID)
        print(
            'submission is available at: <a href="https://codepost.io/code/{}">codepost.io/code/{}</a>'.format(subID, subID))


def uploadNotebooksToCodePost(input_dir, assignment):
    """ Uploads notebooks to codepost """
    for file in os.listdir(input_dir):
        if(file.endswith(".ipynb")):
            try:
                # Files are formatted as email_assignment.ipynb
                idx = file.rfind("_")
                # Taking into account possibility of "_" in email
                student_email = file[:idx]
                # new_file_name = file[idx+1:]
                nb_file_path = input_dir+'/'+file
                notebook = readNotebook(nb_file_path)
                uploadCode(notebook, student_email, assignment)
                print("Uploaded Notebook")
            except Exception as e:
                print("❌!!ERROR!!❌:" + str(e))


def checkSysArgs():
    """ Checks to see if the right amount of parameters are passed by command line """
    if len(sys.argv) < 3:
        raise Exception(
            "There are missing parameters. The following are necessary Input Directory, Output Direcory, Assignment Name")


def getAssignmentData(assignmentName, courseID = COURSE_ID):
    course = codepost.course.retrieve(id=courseID)
    assignment = course.assignments.by_name(assignmentName)
    return assignment


def startProcess(input_dir, assignment_name, ok_line_mode="comment"):
    """ Runs all of the processing """
    assignment = getAssignmentData(assignment_name)
    uploadNotebooksToCodePost(input_dir, assignment)


if __name__ == "__main__":
    """ If this is run from the command line it will automatically process the notebooks. """
    checkSysArgs()
    input_dir, assignment_name, *rest = sys.argv[1:]
    startProcess(input_dir, assignment_name)
