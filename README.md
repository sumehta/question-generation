# Question Generation from Declarative Sentences #

*Update: If you have a feature request please open an issue and I might implement it, or feel free to submit a pull request.*

Given a statement of text such as,
>Handheld devices find ways to bolster U.S. homeland defense and response.

The questions generated will be:
>What do handheld devices find?

The original code is a product of the PhD thesis of Michael Heilman. The original code is written in Java and other resources can be found [here](http://www.cs.cmu.edu/~ark/mheilman/questions/).

For all Pythonistas out there this repository provides a Python wrapper to simplify the execution of the code above.
The hardest part of the whole project is setup. Yes you heard it right.

**Setup**

To run this code you need to have a Java Runtime Environment installed. Java downloads can be found on the Oracle website [here](https://www.java.com/en/download/manual.jsp). Version 1.6.0_07 of Java was used in developing the original system. The code is packaged up for use on UNIX systems, or for use in the Eclipse IDE.

*Dependencies*

The following are the dependencies of the original code.

-Apache Commons Lang (http://commons.apache.org/lang/)

-Apahce Commons Logging (http://commons.apache.org/logging/)

-JUnit (http://www.junit.org/)

-JWNL (http://sourceforge.net/projects/jwordnet/)

-Stanford NLP tools (http://www-nlp.stanford.edu/software/)

-WordNet (http://wordnet.princeton.edu/)

-The sst-light-0.4 release of the SuperSenseTagger, from which we used the SemCor data for training the supersense tagger (http://sourceforge.net/projects/supersensetag/)

-The Semcor corpus, used for training the supersense tagger (http://www.cse.unt.edu/~rada/downloads.html#semcor)

-The WEKA toolkit, version 3.6.0 (http://www.cs.waikato.ac.nz/ml/weka/)


The good news is that you don't need to download each one of those individually because everything is neatly packed in the **QuestionGeneration.zip** bundled with the code.

1. First, clone this repository,

	`git clone https://github.com/sumehta/question-generation.git`

2. Unzip the **QuestionGeneration.zip** file

	`unzip QuestionGeneration.zip`

	`cd QuestionGeneration`

3. [Optinal] Start two servers to speed up the script, Stanford Parser server and the SST servers in two separate terminals.

	`bash runStanfordParserServer.sh`

	`bash runSSTServer.sh`

4. Finally, to get a list of questions for a statement, execute this command

	`python question.py -s 'Handheld devices find ways to bolster U.S. homeland defense and response'`


For other options exposed by the script type,

`python question.py -help`

For developers, I have also included a QuestionGenerator class, that exposes other methods for processing large collections.

*Note: This repository is still in dev and I'll be exposing more options exposed by the original system.*
