"""
Notebook Submission Process:
1. Instantiate codepost object with API Key from hidden config file
2. Get assignment object from assignment name
3. Submission:
    - Get submission ID
        - If submission doesn't exist for the student, create a new submission
        - If submission does exist for student, get that submission id
4. Read Notebook as a string from the correct directory
    - TODO: plan for the file structure on the server environment
5. Submit file using submission ID -- Print submission confirmation with URL
"""


def submit(studentEmail, assignmentName):
    from IPython.core.display import display, HTML
    import codepost
    COURSE_ID = 345

    course = codepost.course.retrieve(id=COURSE_ID)
    assignment = course.assignments.by_name(assignmentName)

    try:
        subID = assignment.list_submissions(student=studentEmail)[0].id
    except:
        subID = codepost.submission.create(
            assignment=assignment.id, students=[studentEmail]).id
    finally:
        print(subID)
        with open("{}.ipynb".format(assignmentName), "r") as assignmentFile:
            code = assignmentFile.read()
            file = codepost.file.create(
                name="Lab1.ipynb", extension="ipynb", code=code, submission=subID)
            print(file.id)
            display(HTML(
                'Your submission is available at: <a href="https://codepost.io/code/{}">codepost.io/code/{}</a>'.format(subID, subID)))
    # return('<a href="https://codepost.io/code/{}">codepost.io/code/{}</a>'.format(subID, subID))
