import { Inject, Injectable } from '@nestjs/common';
import { ClientProxy } from '@nestjs/microservices';
import { Cron, CronExpression } from '@nestjs/schedule';
import { pr } from './app.module';

@Injectable()
export class AppService {

  constructor(
    @Inject('COMMUNICATION') private readonly communicationClient: ClientProxy,
  ) {}

  getHello(): string {
    this.communicationClient.emit("test", 'getHello');
    return "Hello";
  }

  test01(): string {
    this.communicationClient.emit("test", 'test01');
    return "Hello";
  }


  // @Cron(CronExpression.EVERY_10_SECONDS,{ name: 'test' })
  // test() {
  //   pr('CronExpression',2222)
  // }

}
