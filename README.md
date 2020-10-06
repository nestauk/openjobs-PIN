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

## Installation and setup
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

The output of this project can be seen <a href = "https://productivityinsightsnetwork.co.uk/app/uploads/2019/08/Nesta_regional_skill_mismatch_reportv2.pdf">here</a>.

The goal of the project is to collect data on travel times using open source software (Open Trip Planner, Open Street Map, etc.) and then compute a measure of job accessibility. We want to know how easy it is for people to reach jobs.

The overall workflow is as follows:
1. Get information on the occupational breakdown of workers by OA from LMI for ALL (<code>Jobs_breakdown_get_data.ipynb</code>). The number of jobs per OAs should already be included in the data folder (it is taken from the Business Register and Employment Survey).
2. Get the centroids for each OA and LSOA using the ONs postcode directory (<code>get_oa_lsoa_centroids.ipynb</code>).
3. Install local instances of Open Trip Planner (OTP) together with PropeR. PropeR is a package released by the ONS Data Science Campus with which to query OTP. Instructions are in the links in the section above.
4. Collect data for the West Midlands for all possible pairs of LSOAs using PropeR and OTP (<code>propeR_get_data.ipynb</code> and <code>propeR_get_data-copy-to-run.ipynb</code>).
5. Analyse the data to compute the job accessibility measures (<code>propeR_analyse_data.ipynb</code>).

It is also possible to analyse commuting distances (from Census 2011): see scripts beginning with <code>commuting_distances</code>.

# Further information
All notes can be found <a href="https://drive.google.com/drive/folders/1bzfw-BjZ7KI8tSUjbGck0w_-0s2rgFaP?usp=sharing">here</a>.

Outputs can be found <a href="https://drive.google.com/drive/folders/1G8XdBoeqFmuLYVqarNgtCJ9zC1NCxA6o?usp=sharing">here</a>.

Copies of (some of) the plots produced can be found <a href="https://drive.google.com/drive/folders/1DJAJ_kNalMXaWqE2wJblP4XnSm8hyerx?usp=sharing">here</a>.
