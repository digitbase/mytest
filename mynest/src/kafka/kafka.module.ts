import { Injectable, Module, OnModuleInit } from '@nestjs/common';
import {Kafka,Producer,ProducerRecord} from 'kafkajs'
import { pr } from 'src/app.module';
import { CatController } from 'src/cat.controller';
import { ConsumerService } from './consumer.service';
import { ProducerService } from './producer.service';

@Module({
  providers: [ProducerService,ConsumerService],
  exports: [ProducerService, ConsumerService],
})
export class KafkaModule {}
