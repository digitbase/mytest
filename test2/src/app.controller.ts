import { Controller, Get, Post } from '@nestjs/common';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get('test2')
  getHello(): string {
    return this.appService.getHello();
  }


  @Post('test2')
  getHello2(): string {
    return '[1,2,3,4]'
  }
}
