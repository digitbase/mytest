import { Module } from '@nestjs/common';
import { EnterPersonModule } from 'src/socket01_app/enterPerson.module';
import { EnterPersonModule2 } from 'src/socket01_app/enterPerson2.module';
import { MyTestController } from './mytest.controller';

@Module({
  imports: [],
  controllers: [MyTestController],
  providers: [EnterPersonModule, EnterPersonModule2],
})
export class VehicleAppModule {}
