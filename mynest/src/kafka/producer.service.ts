import { Injectable, Module, OnModuleInit } from '@nestjs/common';
import {Kafka,Producer,ProducerRecord} from 'kafkajs'
import { pr } from 'src/app.module';


@Injectable()
export class ProducerService implements OnModuleInit  {
  private readonly kafka = new Kafka({
    brokers:['10.200.52.235:9092'],
  });
  private readonly producer: Producer = this.kafka.producer();


  async onModuleInit() {
    await this.producer.connect();
    pr("......connect kafka server success.....", 2233)
  }

  async produce(record: ProducerRecord) { 
    await this.producer.send(record);
  }

  async OnApplicationShutdown() {
    await this.producer.disconnect();
    
  }
}