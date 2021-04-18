# Contributing Guidelines
This document contains a set of guidelines for contributing to our project. 

## Code of Conduct
By participating in this project, you are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md). 
Please report behavior that violates our Code of Conduct to [dineline.cs.gy.9223@gmail.com](mailto:dineline.cs.gy.9223@gmail.com)

## Reporting Bugs
This section guides you through reporting any bugs you find. Following these guidelines will make it easier for maintainers to understand your report and reproduce the issue.

### Before Submitting A Bug Report
* Check "How to set up local environment" section in our [README](README.md) file to make sure you set up your environment and configured the application correctly.
* Check our current open issues to make sure the problem hasn't already beed reported. If you find that it already exists and is open, just add a comment to the existing issue instead of opening a new one.

### Submitting A Bug Report
Bugs are tracked as [GitHub issues](https://guides.github.com/features/issues/).
* Use a clear and descriptive title for the issue to identify the problem.
* Outline the exact steps that reproduce the problem. Be as detailed as possible and provide screenshots if possible.
* Describe the behavior that occurred after following the steps and describe what the problem is with that behavior.
* Explain what behavior you expected to happen and why.

## Ways to Contribute
You can contribute in the following two ways:

### 1. Workflow for contributing code
   1. Make a fork of this project. Then, make your changes in your fork.
   2. Ensure that you include unit tests for your feature, as well as integration tests for any existing code that might be impacted.
   3. Check you are using consistent style by running  in the project root folder `python -m black ./` and `python -m flake8 ./` and make all recommended changes. Then run your tests with `python manage.py test` and fix any errors. 
   4. Add the files you changed to our project by creating a Pull Request from your fork. [Refer here](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork) if you want to know more about how this works.
   5. Please keep in mind that your commits should be [atomic](https://en.wikipedia.org/wiki/Atomic_commit#Atomic_commit_convention) and the diffs should be easy to read/understand. This will help in improving the maintainability of our project.

### 2. Contributing your time in other ways

  1. **Writing / improving documentation**: Our documentation exists solely on GitHub, majorly in the [README file](README.md). If you see a misspelling, adding some missing documentation or any other ways to improve it please free to edit it and submit a Pull Request.  

  2. **Reviewing Pull Requests**: Another useful way to contribute to our project is to review other peoples Pull Rrequests. 
