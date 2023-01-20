import {
  Injectable,
  Module,
  OnApplicationShutdown,
  OnModuleInit,
} from '@nestjs/common';
import {
  Kafka,
  Producer,
  Consumer,
  ProducerRecord,
  ConsumerRunConfig,
  ConsumerSubscribeTopics,
} from 'kafkajs';
import { pr } from 'src/app.module';
import { ConsumerService } from './consumer.service';

@Injectable()
export class DahuaConsumer implements OnModuleInit {
  constructor(private readonly consumerService: ConsumerService) {}

  async onModuleInit() {
    let config = {
      eachMessage: async ({ topic, partition, message }) => {
        pr({
          value: message.value.toString(),
          topic: topic.toString(),
          partition: partition.toString(),
        });
      },
    };

    // await this.consumerService.consumer({ topic: 'Dahua_002' }, config);
    // pr('......connect consumer  success.....', 34455);
  }
}
