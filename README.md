#  Machine Learning Engineer Nanodegree

## Capstone Proposal
Nathan Gilbert
June 29th, 2019

## Proposal: Web-based Documentation Summarization

### Domain Background

Everyday we are bombarded with more information than is possible to process.
Identifying and summarizing relevant information in a given document is a task
that can help reduce the time required for acquiring and acting on new
information. Summaries can reduce reading time and personalized summaries can
help a reader better understand material they care about most.

There has been significant work in the field of Document Summarization over the
past two decades. In the early 2000s, a set of conferences named DUC (Document
Understanding Conference) focused on text understanding and summarization and
provided many of the standard data sets still used today. Researchers such as
Daniel Marcu and Inderjeet Mani have written several books and academic papers
on the subject detailing machine learning approaches throughout the early 200s
and 2010s. Recently, the Google Brain team have seen some large gains with
their Transformer and XLNet based systems: <https://github.com/zihangdai/xlnet>
Microsoft Word even provides some basic automatic text summarization capabilities.

My personal motivation for studying this topic is its relevance to Natural
Language Understanding. Identifying the most salient points of an article or
chunk of information is one step of the way to automatically _understanding_
the information an author is attempting to convey.

### Problem Statement

This goal of the project is to provide an endpoint that accepts an http request
with a text document containing 1000 words or less. The endpoint will process
the document with a trained model and return a short summary of the most
important topics from the document. The summary could be a sentence from the
document itself or potentially a set of phrases from the document that best
encapsulate the central theme of the document.

### Datasets and Inputs

The ideal input for this project are news articles. No particular domain of news
articles is specified for this endpoint though I expect there to be differences
in performance that can be attributed to differences between article domains
(e.g. sports vs tech).

For training the model, there several available datasets. The DUC 2003 and DUC
2004 sets are the standard sets that many research uses as a baseline. The DUC
was created specifically for the conferences and research into question
answering and document summarization specifically. The 2003 and 2004 datasets
are the ones most often used in summarization work, with the 2003 used for
testing and the 2004 set used for testing. The DUC dataset is general news
stories which is a good fit for the problem.

For additional training on news article domains there is the CNN/DailyMail data
set that is freely available: <https://cs.nyu.edu/~kcho/DMQA/> as well as the
Cornell Newsroom dataset <https://summari.es>. These would be good additional
training data or

### Solution Statement

It would be beyond the scope of this project and class to attempt to produce new
results on this problem beyond the State-of-the-art examples from publications
such as <http://www.lrec-conf.org/proceedings/lrec2014/pdf/1093_Paper.pdf>.

Instead, it is my intention to implement an already existing solution to the
documentation summarization problem and modify it for use on the web as a hosted
endpoint. My goal is to implement a model based on the _RegSum_ system as
defined in the previous paper. _RegSum_ is a supervised summarization system
that uses weights from 3 unsupervised approaches as well as typical natural
language features such as part-of-speech tags and named entities. This solution
will produce measurable, short summaries of the input news articles.

### Benchmark Model

There are several models described in
<http://www.lrec-conf.org/proceedings/lrec2014/pdf/1093_Paper.pdf>  which could
be used a reference for the performance of the model I intend to build for this
project. The _FreqSum_ model is simple to implement (simply being a measure of
the approximate importance of words in the input based on their frequency.)

### Evaluation Metrics

The standard metric used for measuring model performance in document
summarization is the ROUGE score <https://en.wikipedia.org/wiki/ROUGE_(metric)>.
This is what I intend to use for quantifying the performance of the deployed
models. The ROUGE score is a measure of the n-gram overlap between the model
generated summary and a gold standard summary. There are different variants of
the ROUGE score, for example, ROUGE-2 is a measure of the bigram overlap between
the machine and human generated summaries. ROUGE-S is a measure of the
skip-bigram overlap, where a skip-bigram is any two words that appear in their
sentence order from the original text.

Alternative, or additional metrics could include measuring the noun phrase chunk
overlap between the machine and human summaries (really this is a variant of
ROUGE) or the Levenshtein distance
<https://en.wikipedia.org/wiki/Levenshtein_distance> between the machine and
human summaries.

### Project Design
_(approx. 1 page)_

In this final section, summarize a theoretical workflow for approaching
a solution given the problem. Provide thorough discussion for what strategies
you may consider employing, what analysis of the data might be required before
being used, or which algorithms will be considered for your implementation. The
workflow and discussion that you provide should align with the qualities of the
previous sections. Additionally, you are encouraged to include small
visualizations, pseudocode, or diagrams to aid in describing the project design,
but it is not required. The discussion should clearly outline your intended
workflow of the capstone project.

-----------

**Before submitting your proposal, ask yourself. . .**

- Does the proposal you have written follow a well-organized structure similar to that of the project template?
- Is each section (particularly **Solution Statement** and **Project Design**) written in a clear, concise and specific fashion? Are there any ambiguous terms or phrases that need clarification?
- Would the intended audience of your project be able to understand your proposal?
- Have you properly proofread your proposal to assure there are minimal grammatical and spelling mistakes?
- Are all the resources used for this project correctly cited and referenced?# mlnd-capstone-project
