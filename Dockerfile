FROM dynverse/dynwrappy:v0.1.0

# install scuba
RUN pip install jinja2
RUN pip install git+https://github.com/dynverse/PySCUBA.git # first install without upgrade of dependencies

# install legacy princurve for now
RUN R -e 'install.packages("devtools", repos = "http://cran.us.r-project.org")'
RUN R -e 'devtools::install_github("dynverse/princurve@69b85ad4709b15e5b40f8541f4b5e2ca9059be3a")'

COPY definition.yml example.h5 run.py /code/

ENTRYPOINT ["/code/run.py"]
