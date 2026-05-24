# Summary

This project is aimed at developing an AI model for predicting band gap energy and photocatalytic activity of perovskite-like oxides based on experimental data.

# Requirements

The project uses Python 3.14.3 and packages listed in "requirements.txt". In addition, one has to obtain Materials Project API key since it is used throughout the project. API key should be assigned to API_KEY variable whenever it is requitred.

# Data

Initial dataset is located in "Data/Perovskite dataset export.xlsx" file and includes two subsets: "Photocatalytic dataset" (dataset collected by the author) and "Photocatalytic dataset 2" (adopted from 10.1016/j.apcatb.2018.09.104)

Before data processing datasets should be prepared (see below)

# Dataset preparation

Dataset contains chemical IDs in various databases that are used to fetch CIF files from them by running "CIF files processing" notebook. In addition, although repository already contains CIF files for many of the samples CIF files for some samples are obtained by manipulating files for other (base) structures. For example, to obtain CIF file for HCa2Nb3O10 one can substitute potasium ions in CIF file for KCa2Nb3O10. Such instructions are written in initial dataset and are also exectured in "CIF files processing" notebook aftrer fetching CIF files from web. It will output modified dataset in "CIF_files_processing_output" folder as well as creates new CIF files in "Data/CIF" folder.

**WARNING : CIFs from Springer Materials database are not fetched automatically in this code, therefore one should either download them manually or use already existing CIF files in "Data/CIF" folder**

# Data processing and ML

This part of the pipeline is placed in "Main" notebook. It reads processed dataset from "CIF_files_processing_output" folder and then performs all necessary data processing steps as well as ML part. Then, there is also a section dedicated to genetic algorithm that tries to search for the most active photocatalyst in Materials Project database. 

# Inference for a given compound

The repository contains trained regression models for band gap and photocatalytic activity prediction (.joblib files). The inference using this model can be done by running "Inference and mattergen dataset creation" notebook. 

# Material generation with MatterGen model

With the same code one can generate a fine-tuning datasets for MatterGen model. Two ways to do this are presented: either use experimental data on photocatalytic activity of oxides from author's dataset (way 1) or predict photocatalytic activity for sampels in MatterGen datasets using trained regression models (way 2).

### Way 1:

Use "Expeiment_dataset_creation_for_mattergen" notebook. Set input_dataset_path variable to the dataset .xlsx file you want to use. We suggest you to use the output of "CIF files processing" notebook as an input but with composition_relative_tolerance set to 0.0001 to prevent unordered structures to get into MatterGen fine-tuning dataset. The "Expeiment_dataset_creation_for_mattergen" notebook outputs dataset for fine-tuning in "mattergen_dataset_for_fine_tuning.csv" file that should be split into train, test, and val datasets. Then follow the README file for MatterGen.

### Way 2:

Use "Inference and mattergen dataset creation" notebook. You need to have "train.csv", "test.csv", "val.csv" datasets downloaded in "Data/Mattergen_dataset/init/" folder. The notebook will produce datasets for fine-tuning into folder "Data/Mattergen_dataset/with_activity/". Then follow the README file for MatterGen.


# Processing MatterGen output

One can use MatterGen output string to convert it to .cif files of generated compunds by using "Mattergen output processing.py" file. You should place MatterGen output string into "structures.txt" file before this. CIF files of generated compounds will be placed into "generated_cifs" folder.

These .cif files then can be used to evaluate photocatalytic activity of generated compounds according to "Inference for a given compound" section.