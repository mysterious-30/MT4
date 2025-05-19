from flask import Flask, request, jsonify
from datetime import datetime
import threading

app = Flask(__name__)

# Store received alerts for monitoring
received_alerts = []
alert_lock = threading.Lock()

@app.route('/alert', methods=['POST'])
def alert():
    try:
        data = request.form
        
        with alert_lock:
            alert_data = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'action': data.get('action'),
                'symbol': data.get('symbol'),
                'price': float(data.get('price', 0)),
                'time': data.get('time')
            }
            received_alerts.append(alert_data)
            
            # Print to console for debugging
            print(f"\nReceived alert: {alert_data}")
            
            # Here you can add your trading logic
            if alert_data['action'] == 'BUY':
                print(">>> Execute BUY logic here <<<")
            elif alert_data['action'] == 'SELL':
                print(">>> Execute SELL logic here <<<")
            
            return jsonify({"status": "success", "message": "Alert processed"}), 200
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get_alerts', methods=['GET'])
def get_alerts():
    with alert_lock:
        return jsonify({"alerts": received_alerts[-50:]}), 200  # Return last 50 alerts

@app.route('/test', methods=['GET'])
def test():
    return "Flask server is running", 200

if __name__ == '__main__':
    print("Starting Flask server on http://127.0.0.1:5000")
    print("Endpoints:")
    print("  POST /alert - Receive trading alerts from MT4")
    print("  GET  /get_alerts - View recent alerts")
    print("  GET  /test - Server test")
    
    app.run(host='127.0.0.1', port=5000, debug=True)