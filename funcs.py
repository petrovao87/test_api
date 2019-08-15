from flask_restful import reqparse

parser = reqparse.RequestParser()

# Process table
parser.add_argument('process_id')# process_id
parser.add_argument('process_name')
parser.add_argument('process_description')
parser.add_argument('activity_flag')
parser.add_argument('process_performer_id')
#
# ProcessParameter table
parser.add_argument('parameter_name')
parser.add_argument('parameter_value')
#
# ProcessStartCondition table
parser.add_argument('condition_type')
parser.add_argument('condition_value')
#
# ProcessPerformer table
parser.add_argument('performer_name')
parser.add_argument('performer_description')
#
# ProcessQuota
parser.add_argument('quota_type')
parser.add_argument('quota_value')


def arg_parse():
    args = parser.parse_args()
    dict_to_update = {}
    for i in args:
        if args[i] is not None:
            dict_to_update[i] = args[i]
    return dict_to_update
