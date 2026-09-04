import pika
import json
import logging


logger = logging.getLogger(__name__)

QUEUE_NAME = "employee_salary_queue"


def publish_employee_id(employee_id: int):
    """
    Sends a message to RabbitMQ containing the employee_id.
    The salary app will read this message and use the ID to
    know a new employee needs a salary record.
    """

    connection = None

    try:
        logger.info(
            "Connecting to RabbitMQ for employee %s",
            employee_id
        )

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )

        channel = connection.channel()

        channel.queue_declare(
            queue=QUEUE_NAME,
            durable=True
        )

        message = json.dumps({
            "employee_id": employee_id
        })

        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=message
        )

        logger.info(
            "Employee %s successfully published to RabbitMQ",
            employee_id
        )

    except pika.exceptions.AMQPConnectionError:
        logger.exception(
            "Could not connect to RabbitMQ for employee %s",
            employee_id
        )
        raise

    except Exception:
        logger.exception(
            "Unexpected RabbitMQ error for employee %s",
            employee_id
        )
        raise

    finally:
        if connection is not None and not connection.is_closed:
            connection.close()
            logger.info("RabbitMQ connection closed")