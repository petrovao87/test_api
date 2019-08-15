from flask import Flask
from flask_restful import Api

from get_and_post_methods import ProcessesList, Processes
from put_methods import ProcessesUpdate, ProcessesParameterUpdate, ProcessesStartConditionUpdate, \
    ProcessesPerformer, ProcessesQuota
from delete_methods import ProcessesDelete


app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Simple test-API</h1>
<h2>test_API</h2>
<p>This application allows you to work with simple API.</p>
<p> For more information visit:
https://github.com/petrovao87/test_api
</p>'''


# Actually setup the Api resource routing here
api.add_resource(ProcessesList, '/api/v1/processes')
api.add_resource(Processes, '/api/v1/processes/<process_id>')
api.add_resource(ProcessesUpdate, '/api/v1/processes/update/process/<process_id>')
api.add_resource(ProcessesParameterUpdate, '/api/v1/processes/update/process_parameter/<process_id>')
api.add_resource(ProcessesStartConditionUpdate, '/api/v1/processes/update/process_start_condition/<process_id>')
api.add_resource(ProcessesPerformer, '/api/v1/processes/update/process_performer/<process_id>')
api.add_resource(ProcessesQuota, '/api/v1/processes/update/process_quota/<process_id>')
api.add_resource(ProcessesDelete, '/api/v1/processes/delete/process/<process_id>')

if __name__ == '__main__':
    app.run()





