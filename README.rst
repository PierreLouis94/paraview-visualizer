==========
Visualizer
==========

.. image:: https://github.com/Kitware/paraview-visualizer/actions/workflows/test_and_release.yml/badge.svg
    :target: https://github.com/Kitware/paraview-visualizer/actions/workflows/test_and_release.yml
    :alt: Test and Release

Visualizer is a Web frontend to ParaView based on trame. The current project is currently incomplete.
You can see it as an alpha version of what it could be. To make it fully functional we need more time and possibly funding.
But rather than waiting for it to be ready to release it, we are putting it out there as it does provide some very good example of what can be done with ParaView and trame.

License
-------

This software is distributed under a BSD-3 license

Requirements 
-----------------------
- Ubuntu 24.04 LTS
- nvm 
- git 
- npm 18

Installing Miniconda
-----------------------
.. code-block:: console
	
	mkdir -p ~/miniconda3
	wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
	bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
	rm -rf ~/miniconda3/miniconda.sh

	~/miniconda3/bin/conda init bash
	~/miniconda3/bin/conda init zsh

Creating the environment
-----------------------
.. code-block:: console

	conda create -n pv-env -c conda-forge python=3.10 trame trame-vtk trame-vuetify trame-components trame-simput
	conda activate pv-env
	conda install -c conda-forge paraview=5.12.1=py310hc2031ef_4_egl
	

	git clone https://github.com/Kitware/paraview-visualizer.git
	cd paraview-visualizer
	export NODE_OPTIONS=--openssl-legacy-provider
	cd vue-components
	npm i
	npm run build
	cd -


Running the application
-----------------------
.. code-block:: console

	# Dein Pfad zum Verzeichnis wo pvpython enthalten ist.
	export PVPYTHON=/home/pierre-louis-bonvin/miniconda3/envs/pv-env/bin/pvpython 
	export TRAME_APP=pv_visualizer.app
	$PVPYTHON -m paraview.apps.trame --data ~
