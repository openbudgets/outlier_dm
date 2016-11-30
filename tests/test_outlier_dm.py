# -*- coding: utf-8 -*-

from .context import outlier_dm

import json
import os
import unittest
import preprocessing_dm as ppdm




class OutlierDetectionLOF(unittest.TestCase):
    """Basic test cases."""

    def test_input_csv_path(self):
        inputCSV = ppdm.ce_from_file_names_query_fuseki_output_csv('noname.csv', os.path.join(os.path.dirname(__file__), '../data'), debug=True)
        assert 'Kilkis_neu.csv' in inputCSV.split('/')
        assert 'outlier_dm' in inputCSV.split('/')

    def test_outlier_detection_LOF(self):
        if os.path.isfile(os.path.join(os.path.dirname(__file__), '../data/Result_top25.csv')):
            os.remove(os.path.join(os.path.dirname(__file__), '../data/Result_top25.csv'))
        inputCSV = ppdm.ce_from_file_names_query_fuseki_output_csv('noname.csv', os.path.join(os.path.dirname(__file__), '../data'), debug=True)
        outlier_dm.detect_outliers_subpopulation_lattice(inputCSV, output_path=os.path.join(os.path.dirname(__file__), '../data'))
        assert os.path.isfile(os.path.join(os.path.dirname(__file__), '../data/Result_top25.csv'))

    def test_outlier_detection_LOF_sparql(self):
        if os.path.isfile(os.path.join(os.path.dirname(__file__), '../data/Result_top25.csv')):
            os.remove(os.path.join(os.path.dirname(__file__), '../data/Result_top25.csv'))
        filename = '+budget-kilkis-expenditure-2012+budget-kilkis-expenditure-2013'
        inputCSV = ppdm.ce_from_file_names_query_fuseki_output_csv(filename, os.path.join(os.path.dirname(__file__), '../data'), debug=False)
        outlier_dm.detect_outliers_subpopulation_lattice(inputCSV, output_path=os.path.join(os.path.dirname(__file__), '../data'))
        assert os.path.isfile(os.path.join(os.path.dirname(__file__), '../data/Result_top25.csv'))


if __name__ == '__main__':
    unittest.main()