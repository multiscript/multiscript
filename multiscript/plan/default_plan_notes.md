# Welcome to Multiscript!

Multiscript documents are called *plans*. You're currently looking at the *default* plan, and reading its plan *notes*. Both the plan and its notes can be edited, or you can create a brand new plan or open an existing plan.

To help you get started, some basic documentation is below. You can find more documentation at [multiscript.app/docs/](https://multiscript.app/docs/)

---

## Plans
A Multiscript plan describes the Bible passage references, Bible versions, output template and settings that will be used to generated the set of output files.

Here are the basic features of a plan:

### Bible Passages
This is the list of Bible passages you want to collate. Many common English abbreviations for book names will be accepted. At the moment, you always have to include the book name (i.e. references like `Mark 1:1-5; 2:1-5` won't work, so use `Mark 1:1-5; Mark 2:1-5` instead).

Passages separated by a comma are considered to be part of one *group*. Usually this means they'll appear in a single table under a combined heading, separated by an ellipsis (...).

Passages separated by a semicolon are considered to be in separate groups (i.e. separate tables).

### Bible Versions
This is the list of versions you wish to combine. Click **Add Versions to Set** to add versions to the plan.

The version *columns* (i.e. Version A, Version B etc.) control how the versions are combined. It's easiest to think of each column in this list as a Bible passage column in your output document. You then tick which versions you want to appear in each column.

For example, a column with just one version ticked means that version will appear in every output document. A column with multiple versions ticked will generate a series of output files – one (or more) for each version. You can have any number of columns (up to 26), and Multiscript will generate every possible combination for the versions and column ticks you enter.

You can double-click on any version to edit its labels, preferred font etc.

### Template
This is the template document that Multiscript will use to generate each output file.

### Output Folder
This is the folder in which the output files will be generated.

### Plan Options
Click this button to adjust various settings specific to this plan file.

### Start
Click this button to execute the plan, which will generate the output files.
