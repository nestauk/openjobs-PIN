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

My own notes on the process can be found <a href="https://docs.google.com/document/d/1i49L1tUjrUdXOATcxlYnvdChUXTQiTfjeBGCMoQ_RCs/edit?usp=sharing">here</a>.

Along the way, there will be the need to install/download many other resources, such as <a href="https://github.com/planarnetwork/dtd2mysql">dtd2mysql</a>.

4. <b>Download geography-related datasets </b> from the Open Geography Portal:
<ol>
<li> List of postcode with centroids (can be downloaded from <a href"https://geoportal.statistics.gov.uk/datasets/ons-postcode-directory-latest-centroids">here</a>). </li>
<li> LSOA2011 Boundaries (can be downloaded from <a href"https://geoportal.statistics.gov.uk/datasets/lower-layer-super-output-areas-december-2011-boundaries-ew-bfc">here</a>) </li>
</ol>

Other files are already included in the directory under <code>data/Map-files</code>, but these were too big.

# Workflow

Get information from LMI for ALL. Have not uploaded mine because it can not be cached.

# Further information
All notes can be found <a href="https://drive.google.com/drive/folders/1bzfw-BjZ7KI8tSUjbGck0w_-0s2rgFaP?usp=sharing">here</a>.

Outputs can be found <a href="https://drive.google.com/drive/folders/1G8XdBoeqFmuLYVqarNgtCJ9zC1NCxA6o?usp=sharing">here</a>.

Copies of (some of) the plots produced can be found <a href="https://drive.google.com/drive/folders/1DJAJ_kNalMXaWqE2wJblP4XnSm8hyerx?usp=sharing">here</a>.
