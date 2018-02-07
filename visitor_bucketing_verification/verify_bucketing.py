import argparse
from optimizely import optimizely

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

test_csv = open(args.path_to_CSV, 'r')
header_line_split= test_csv.readline().strip().split(',')
assert(header_line_split[0] == 'visitorId')
assert(header_line_split[1] == 'variationId')

with open(args.path_to_datafile, 'r') as local_datafile:
    datafile = local_datafile.read()

optimizely_client = optimizely.Optimizely(datafile)
experiment = optimizely_client.config.get_experiment_from_key(args.experiment_key)
variation_key_to_id_map = dict()
variation_id_to_key_map = dict()
variation_counter_map = dict()
for variation in experiment.variations:
    variation_key_to_id_map[variation['key']] = variation['id']
    variation_id_to_key_map[variation['id']] = variation['key']
    variation_counter_map[variation['key']] = 0

test_line = test_csv.readline().strip()
line_count = 0
bucketing_errors = False
while test_line:
    line_count += 1
    split_line = test_line.split(',')
    visitor_id = split_line[0].strip()
    expected_variation_id = split_line[1].strip()

    bucketed_variation_key = optimizely_client.get_variation(args.experiment_key, visitor_id)
    if not expected_variation_id == variation_key_to_id_map[bucketed_variation_key]:
        bucketing_errors = True
        print('Assertion FAILED in line ' + str(line_count))
        print('Visitor "' + visitor_id + '" should have been in variation "' + bucketed_variation_key +
            '", but was recorded as being in variation "' + variation_id_to_key_map[expected_variation_id] + '".')
        bucketing_key = visitor_id + experiment.id
        bucket_value = optimizely_client.decision_service.bucketer._generate_bucket_value(bucketing_key)
        print('Visitor "' + visitor_id + '" should have been bucketed into bucket ' + str(int(bucket_value)) + '.')

    variation_counter_map[bucketed_variation_key] += 1

    test_line = test_csv.readline()

if bucketing_errors:
    print('Visitors FAILED to be successfully bucketed!')
else:
    print('Visitors successfully bucketed!')

for key in variation_counter_map:
    print(str(variation_counter_map[key]) + ' visitors should have been in variation "' + key + '".')
