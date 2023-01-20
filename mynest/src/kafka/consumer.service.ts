import { Injectable, Module, OnApplicationShutdown, OnModuleInit } from '@nestjs/common';
import {Kafka,Producer, Consumer,ProducerRecord, ConsumerRunConfig,ConsumerSubscribeTopic} from 'kafkajs'
import { pr } from 'src/app.module';


@Injectable()
export class ConsumerService implements OnModuleInit  {
  private readonly kafka = new Kafka({
    brokers:['10.200.52.235:9092'],
  });
  private readonly consumers: Consumer [] = []


  async onModuleInit() {

    pr("......connect consumer  success.....", 2233)
  }

  async consumer(topic: ConsumerSubscribeTopic, config: ConsumerRunConfig) { 
    const consumer = this.kafka.consumer({
      groupId: "hc-command-screen-consumer"
    })
    await consumer.connect();
    await consumer.subscribe(topic);
    await consumer.run(config);
    this.consumers.push(consumer);
  }
  
  async OnApplicationShutdown(signal?: string) {
    for (const consumer of this.consumers) { 
      await consumer.disconnect();
    }
  }

}