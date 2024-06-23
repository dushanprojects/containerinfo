# Import necessary libraries and modules
from kubernetes import client, config
from flask import Flask, request, jsonify
import json

# Initialize Flask application
app = Flask(__name__)

# Load Kubernetes configuration from within the cluster
config.load_incluster_config()

# Define a route for the container-resources endpoint
@app.route('/container-resources', methods=['GET'])
def get_container_resources():
    # Get the pod-label query parameter from the request
    pod_label_param = request.args.get('pod-label')
    
    # If the pod-label parameter is not provided, return an error response
    if not pod_label_param:
        return jsonify({'error': 'pod-label query parameter is required lable name and value'}), 400

    try:
        # Split the pod-label parameter into label and value
        label, value = pod_label_param.split('=')
    except ValueError:
        # Return an error if the pod-label parameter is not in the correct format
        return jsonify({'error': 'pod-label must be in the format key=value'}), 400

    # Initialize Kubernetes API client
    v1 = client.CoreV1Api()
    # Init Pod information list (all namespaces)
    pod_info = []
    try:
        # Get all namespaces
        namespaces = v1.list_namespace().items

        for namespace in namespaces:
            # Get pods in current namespace
            pods = v1.list_namespaced_pod(namespace.metadata.name).items

            # Process pods in the current namespace
            for pod in pods:
                # Filter by user-specified pod label and value
                if pod.metadata.labels.get(label) == value:
                    for container in pod.spec.containers:
                        # Set Default values for missing resources (requests/limits)
                        mem_req = 'None'
                        mem_limit = 'None'
                        cpu_req = 'None'
                        cpu_limit = 'None'

                        # Check if container resources exist
                        if container.resources:  
                            # Handle empty requests/limits dictionaries
                            requests = container.resources.requests or {}
                            limits = container.resources.limits or {}

                            # Get Memory/CPU request/limits if available
                            mem_req = requests.get('memory', mem_req)
                            mem_limit = limits.get('memory', mem_limit)
                            cpu_req = requests.get('cpu', cpu_req)
                            cpu_limit = limits.get('cpu', cpu_limit)

                        # Format POD dictionary
                        pod_dict = {
                            "container_name": container.name,
                            "pod_name": pod.metadata.name,
                            "namespace": pod.metadata.namespace,
                            "mem_req": mem_req,
                            "mem_limit": mem_limit,
                            "cpu_req": cpu_req,
                            "cpu_limit": cpu_limit
                        }
                        # Add pod information to the list
                        pod_info.append(pod_dict)

        # Return pod information within the specified label and value (filtered) as JSON
        return app.response_class(
            response=json.dumps(pod_info, indent=4),
            mimetype='application/json' #Print JSON output one after another
        ), 200
    
    # Return error if API call fails
    except client.exceptions.ApiException as e:
        return jsonify({'error': f"Error retrieving pods: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)