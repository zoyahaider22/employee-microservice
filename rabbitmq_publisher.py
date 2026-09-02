import pika
import json

QUEUE_NAME = "employee_salary_queue"


def publish_employee_id(employee_id: int):
    """
    Sends a message to RabbitMQ containing the employee_id.
    The salary app will read this message and use the ID to
    know a new employee needs a salary record.
    """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        message = json.dumps({"employee_id": employee_id})
        channel.basic_publish(exchange="", routing_key=QUEUE_NAME, body=message)

        connection.close()
        print(f"[employee_app] Sent to RabbitMQ: {message}")
    except Exception as e:
        print(f"[employee_app] Could not send message (is RabbitMQ running?): {e}")