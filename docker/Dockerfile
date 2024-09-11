FROM kitware/trame:py3.10-glvnd
  
RUN install -d -o trame-user -g trame-user /deploy
  
ARG PV_URL='https://www.paraview.org/files/v5.13/ParaView-5.13.0-egl-MPI-Linux-Python3.10-x86_64.tar.gz'
RUN mkdir -p /opt/paraview && cd /opt/paraview && wget -qO- $PV_URL | tar --strip-components=1 -xzv
ENV TRAME_PARAVIEW=/opt/paraview
ENV TRAME_CLIENT_TYPE=vue2
  
COPY --chown=trame-user:trame-user . /deploy
  
RUN /opt/trame/entrypoint.sh build
