#######################################################################################
## DO NOT EDIT THIS FILE! This file was automatically generated from the dockerfile. ##
## Run babelwhale::convert_dockerfile_to_singularityrecipe() to update this file.    ##
#######################################################################################

Bootstrap: shub

From: dynverse/dynwrap:py3.6

%labels
    version 0.1.4

%files
    . /code

%post
    chmod -R 755 '/code'
    apt-get update && apt-get install -y r-base
    pip install rpy2
    pip install jinja2
    pip install git+https://github.com/dynverse/PySCUBA.git 
    pip install git+https://github.com/dynverse/PySCUBA.git --upgrade --no-dependencies --no-cache-dir -U 
    R -e 'install.packages("devtools", repos = "http://cran.us.r-project.org")'
    R -e 'devtools::install_github("dynverse/princurve@69b85ad4709b15e5b40f8541f4b5e2ca9059be3a")'

%runscript
    exec python /code/run.py

