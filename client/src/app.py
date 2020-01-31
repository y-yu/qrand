from flask import Flask, render_template, send_from_directory, request
from random import Random
from .repository import quantum, qrand_api_caller
from .service import generate_post, verify_random, send_cheat_state
from .controller import measure, verify, cheat

app = Flask(__name__)

@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('assets', path)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# DI配線をする。
random_impl = Random()
gen_quantum_repository = quantum.GenerateQuantumStateRepository(random_impl)
send_qubit_repository = qrand_api_caller.QRandApiRepository()
gen_post_service = generate_post.GenerateAndPostService(send_qubit_repository, gen_quantum_repository)
verify_random_service = verify_random.VerifyRandomService(send_qubit_repository)
send_cheat_service = send_cheat_state.PostCheatStateService(random_impl, send_qubit_repository)
measure_controller = measure.MeasureRequestController(gen_post_service)
verify_controller = verify.VerifyRequestController(verify_random_service)
cheat_controller = cheat.CheatController(random_impl, send_cheat_service, verify_random_service)

@app.route('/measure', methods=['GET'])
def measure():
    return measure_controller.render()

@app.route('/cheat', methods=['GET'])
def cheat():
    return cheat_controller.measure_with_cheat()

@app.route('/verify', methods=['POST'])
def verify():
    json_request = request.get_json(force = True)
    return verify_controller.render(json_request)

@app.route('/cheat_verify', methods=['POST'])
def cheat_verify():
    json_request = request.get_json(force=True)
    return cheat_controller.verify_with_cheat(json_request)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
