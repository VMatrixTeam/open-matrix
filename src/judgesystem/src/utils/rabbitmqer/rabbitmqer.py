#_*_coding=utf-8_*_
import pika

class Rabbitmqer():
  @staticmethod
  def sendMessage(**kwargs):
      try:
          conn = pika.BlockingConnection(pika.ConnectionParameters(host = kwargs["host"]))
          del kwargs["host"]
          channel = conn.channel()
          channel.queue_declare(queue=kwargs["routing_key"],durable=True,exclusive=False)
          channel.basic_publish(**kwargs)
      except:
          return False
      return True
