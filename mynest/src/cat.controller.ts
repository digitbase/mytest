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
@Controller()
export class CatController implements OnModuleInit{

  async onModuleInit() {
  }

  constructor(private readonly CatService: CatService,
    private gateWay01: EnterPersonModule,
    private gateWay02: EnterPersonModule2,  
  ) { }

  @MessagePattern('Dahua_002')
  async DEVICE_ALARM(@Payload() message: any, @Ctx() context: KafkaContext) {
    // let res = message.value.eventData;
    pr(message);

    return message;
  }



  @MessagePattern('Dahu_002') // Our topic name
  async getHello2(@Payload() message) {
    console.log(message.value);
    pr(message,222)
    return 'Hello World';
  }


  @Get("/cat")
  async getHello() {
    let msg = {
      topic: "test",
      msg:"nihao",
    }
    let str = JSON.stringify(msg);
    let res1 = await this.gateWay01.pushMsg(str);
    let res2 = await this.gateWay02.pushMsg(str);

    return this.CatService.getHello();

  }


  @Get('/cat/:id')
  getHellow2222() : string{
    return 'bbbb'
  }


}
