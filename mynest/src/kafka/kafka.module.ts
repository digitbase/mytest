import { Injectable, Module, OnModuleInit ,Inject} from '@nestjs/common';
import { pr } from 'src/app.module';
import { ClientKafka, ClientProvider, ClientsModule, Transport } from '@nestjs/microservices';
@Module({
  imports: [
    ClientsModule.registerAsync([
      {
        useFactory: async (): Promise<ClientProvider> => {
          return {
            transport:Transport.KAFKA,
            options: {
              client: {
                clientId: "hc-command-screen",
                brokers: ['10.200.52.235:9092']
              },
              consumer:{
                groupId: 'hc-command-screen-consumer'
              }
            }
          }
        },
        name: 'HERO_SERVICE',
      }
    ]),
  ]
})
export class KafkaModule {
  @Inject("HERO_SERVICE")
  kafkaClient: ClientKafka;

  constructor(){
    console.log("init KafkaModule")
  }
  async onModuleInit() {

    await this.kafkaClient.connect().then(res => {
      console.log('......connect kafka server success......');
      pr(res,222200)
    });
  }
}
