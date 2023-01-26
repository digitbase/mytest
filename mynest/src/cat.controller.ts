import { Controller, Get, OnModuleInit } from '@nestjs/common';
import { CatService } from './cat.service';
import { EnterPersonModule } from './socket01_app/enterPerson.module';
import { EnterPersonModule2 } from './socket01_app/enterPerson2.module';
import {
  Client,
  ClientKafka,
  Ctx,
  KafkaContext,
  MessagePattern,
  Payload,
  Transport,
} from '@nestjs/microservices';
import { pr } from './comm/fun.comm';
import { ConsumerService } from './kafka/consumer.service';
import { AppService } from './app.service';
import { Cron,CronExpression,SchedulerRegistry } from '@nestjs/schedule';
@Controller()
export class CatController implements OnModuleInit{

  async onModuleInit() {
    pr("CatController init", 6655)
  }

  constructor(
    private readonly CatService: CatService,
    private readonly appService: AppService,
    private gateWay01: EnterPersonModule,
    private gateWay02: EnterPersonModule2,  
  ) { }

  @MessagePattern('Dahua_002')
  async DEVICE_ALARM(@Payload() message: any, @Ctx() context: KafkaContext) {
    // let res = message.value.eventData;
    pr(message);

    return message;
  }

  // @Cron(CronExpression.EVERY_10_SECONDS,{ name: 'test' })
  // test() {
  //   pr('CronExpression',1111)
  // }

  @MessagePattern('Dahu_002') // Our topic name
  async getHello2(@Payload() message) {
    console.log(message.value);
    pr(message,222)
    return 'Hello World';
  }


  @Get("/cat")
  async getHello() {
    this.appService.test01();
    pr("cat",222)

  }


  
  @Get('/cat/:id')
  getHellow2222() : string{
    return 'bbbb'
  }


}
