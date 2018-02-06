import argparse

parser = argparse.ArgumentParser(description='Verify visitors have been bucketed correctly '
                                             'for an Optimizely Experiment.')
parser.add_argument('experiment_key',
                    type=str,
                    help='The name of the experiment to check bucketing in.')
parser.add_argument('path_to_CSV',
                    type=str,
                    help='The relative path to the .csv file containing visitorIds and variationIds to check.')
parser.add_argument('path_to_datafile',
                    type=str,
                    help='The relative path to a local datafile to check bucketing with. '
                         'Must pe present if no datafile URL is supplied.')

args = parser.parse_args()



