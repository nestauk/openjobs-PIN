# About the project
This project analysed the entire corpus (as of 2019) of National Occupational Standards (NOS) for Skills Development Scotland.

## Authors

Stef Garasto, Jyldyz Djumalieva

# Prerequisites
<ol>
<li> Python 3.6 and (ideally) Conda. </li>
<li> (If possible) API credentials for TransportAPI and Google Maps. </li>
</ol>

# Getting started

## Installation
1. <b> Clone the repo. </b> In a terminal, after navigating to the folder where you want to install the skill_demand repo, type:

<code>
git clone https://github.com/nestauk/openjobs-PIN.git
</code>

2. <b> Create the conda environment. </b> The easiest way is the following. In a terminal, first navigate to the project folder. You are in the right folder, if it contains a file called <code> conda_environment.yaml</code>. Then type:

<code>conda env create -f conda_environment.yaml</code>

Note that the environment will be called "transport". If you want to give it a different name, then you need to make a copy of the file <code>conda_environment.yaml</code>, change the name in the first line of the new file and run the command above with the name of the new file. Making a copy means that it can be pushed to github without overriding the main file (better yet, if it's in a separate branch).

3. <b> Install a local instance of Open Trip Planner and PropeR. </b>
Resources and instructions on how to do it can be found on these Github repositories by the ONS Data Science Campus:
<ol>
<li> https://github.com/datasciencecampus/access-to-services </li>
<li> https://github.com/datasciencecampus/proper </li>
<li> https://github.com/datasciencecampus/graphite </li>

Along the way, there will be the need to install/download many other resources, such as <a href="https://github.com/planarnetwork/dtd2mysql">dtd2mysql</a>.

# Workflow
