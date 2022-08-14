import { Module } from '@nestjs/common';
import {MyTestController} from './mytest.controller';

@Module({
  imports: [],
  controllers: [
    MyTestController
  ],
  providers: [],
})
export class VehicleAppModule {}
