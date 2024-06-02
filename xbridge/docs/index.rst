XBridge (eba-xbridge)
#####################

Overview
============
XBridge is a Python library which main function is to convert XBRL-XML files into XBRL-CSV files by using EBA's taxonomy.
It works only with EBA Taxonomy upon version |eba_version|. For future versions, library must be updated.

Installation
============

To install the library, run the following command:

.. code:: bash

    pip install eba-xbridge


How XBridge works:
=========================

Firstly, an XBRL-XML file has to be selected to convert it. Then, that XBRL-XML file is input in the following function contained in the ``API`` package:

.. code:: python

  >>> from xbridge.api import convert_instance

  >>> convert_instance(input_path, output_path)

The sources to do this process, as it was indicated before, are two: The ``XML-instances`` and EBA´s taxonomy.

#######
Index
#######

.. toctree::
    :maxdepth: 2

    api.rst
    converter.rst
    taxonomy_loader.rst
    technical_notes.rst
    modules.rst
    xml_instance.rst
