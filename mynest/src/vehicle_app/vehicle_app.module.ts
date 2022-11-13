import { Module } from '@nestjs/common';
import { MyTestController } from './mytest.controller';
import { PhotoController } from './photo.controller';
import { EmployeeController } from './employee.controller';

@Module({
  imports: [],
  controllers: [
    MyTestController,
    // EmployeeController,
  ],
  providers: [],
})
export class VehicleAppModule {}
