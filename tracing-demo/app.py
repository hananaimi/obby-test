from flask import Flask, request, jsonify
import logging
from random import randint # randint is not used in the provided code, but kept if you intend to use it later

# Import for Prometheus metrics exposure
from prometheus_flask_exporter import PrometheusMetrics

# OpenTelemetry imports for manual instrumentation (tracer)
from opentelemetry import trace
# When using OpenTelemetry Operator for auto-instrumentation,
# explicitly setting a TracerProvider like this is usually not needed
# as the operator handles it. Removing the lines below resolves
# the "Overriding of current TracerProvider is not allowed" warning.
# from opentelemetry.sdk.trace import TracerProvider

# Configure Flask app
app = Flask(__name__)

# Initialize PrometheusMetrics to expose /metrics endpoint
# This will automatically collect basic process metrics and expose them
# at the /metrics endpoint on your Flask application.
metrics = PrometheusMetrics(app)

# You can also add custom metrics if needed, for example:
# from prometheus_client import Gauge
# my_custom_gauge = Gauge('my_app_total_requests', 'Total number of requests to my application')
# metrics.register_default(my_custom_gauge) # Register it with the Flask exporter


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the tracer; with auto-instrumentation, this will be provided by the agent.
tracer = trace.get_tracer(__name__)

def generate_metadata():
    """ Helper function to generate trace, span metadata from current context """
    current_span = trace.get_current_span()

    # Get trace_id and span_id from the current span context
    trace_id = format(current_span.get_span_context().trace_id, "032x")
    span_id = format(current_span.get_span_context().span_id, "016x")

    metadata = {
        "trace_id": trace_id,
        "span_id": span_id,
        "http_target": request.path,
        "http_method": request.method
    }
    return metadata

def log_metadata(metadata):
    """ Logs the generated metadata """
    logger.info(f"Response metadata: {metadata}")

@app.route("/")
def index():
    """
    Root endpoint for the application.
    Generates metadata and returns a welcome message.
    """
    metadata = generate_metadata()
    metadata["message"] = "Welcome to OpenTelemetry Instrumented App!"

    log_metadata(metadata)
    return jsonify(metadata)


@app.route("/home")
def manual_tracing():
    """
    Endpoint demonstrating manual OpenTelemetry tracing.
    A new span 'manual_span' is created here.
    """
    # Manually create a span
    with tracer.start_as_current_span("manual_span") as span:
        # Set attributes on the manually created span
        span.set_attribute("http.target", request.path)
        span.set_attribute("http.method", request.method)
        span.set_attribute("env", "development")

        # Generate metadata for manual instrumentation
        metadata = generate_metadata()
        metadata["message"] = "This is manually instrumented!"
        metadata["env"] = "Development"

        log_metadata(metadata)
        return jsonify(metadata)

@app.route("/shop")
def auto_tracing():
    """
    Endpoint for a simulated shopping page, relying on auto-instrumentation
    to capture tracing information for the request.
    """
    metadata = generate_metadata()
    metadata["message"] = "Welcome To Our Online Shopping"

    log_metadata(metadata)
    return jsonify(metadata)

@app.route("/blog")
def blog():
    """
    Endpoint for a simulated blog page, also relying on auto-instrumentation.
    """
    metadata = generate_metadata()
    metadata["message"] = "Welcome, Find Latest News Here!"

    log_metadata(metadata)
    return jsonify(metadata)

if __name__ == "__main__":
    # In a Kubernetes environment with auto-instrumentation, Flask applications
    # are often run using a WSGI server like Gunicorn.
    # For local testing, app.run() is fine.
    app.run(host='0.0.0.0', port=8080)
