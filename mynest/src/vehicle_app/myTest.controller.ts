import { Controller, Body, Post, Get, Query } from '@nestjs/common';
import { EnterPersonModule } from 'src/socket01_app/enterPerson.module';
import { EnterPersonModule2 } from 'src/socket01_app/enterPerson2.module';

export class ParamsInput {
  id: string;
  isPublic: boolean;
}

@Controller('/test')
export class MyTestController {
  constructor(
    private gateWay01: EnterPersonModule,
    private gateWay02: EnterPersonModule2,
  ) {}
  @Post()
  async queryVehiclePermissionInfo(@Body() input): Promise<any> {
    console.log(input);
    return { 1: 1 };
  }
  @Get('/say')
  async getInfo(@Query() input): Promise<any> {
    let msg = {
      topic: 'test',
      msg: 'MyTestController',
    };
    let str = JSON.stringify(msg);
    let res1 = await this.gateWay01.pushMsg(str);
    let res2 = await this.gateWay02.pushMsg(str);
    console.log(input);
    return { 'input ': input };
  }

  @Post('/say2')
  async getInfo2(@Body() input: ParamsInput): Promise<any> {
    console.log(input);
    return { 'input ': input };
  }
}
