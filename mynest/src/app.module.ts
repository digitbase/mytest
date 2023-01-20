import { Module ,OnModuleInit} from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { CatController } from './cat.controller';
import { CatService } from './cat.service';
import { EnterPersonModule } from './socket01_app/enterPerson.module';
import { EnterPersonModule2 } from './socket01_app/enterPerson2.module';
import { VehicleAppModule } from './vehicle_app/vehicle_app.module';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ConfigModule } from '@nestjs/config';
import configuration from './config/database.config';
import {EmployeeModule} from './vehicle_app/employee.module'
import { KafkaModule } from './kafka/kafka.module';
import { DahuaConsumer } from './kafka/dahua.consumer';
import { ClientKafka, ClientProvider, ClientsModule, Transport } from '@nestjs/microservices';
import { ConsumerService } from './kafka/consumer.service';

export function pr(input:any, type2?:number):void{
	console.log(typeof input, "==>",input);let _type = type2?type2:0;let str = " "
	if (_type > 0) {for(let i=0; i < 20; i++)  str +=_type.toString()+" ";console.log(`==============    ${str}    ===============`)}
}

const env = process.env.ENV_NODE || '';

// pr(process,1)
// pr(process.env.ENV_NODE,2)
// pr(__dirname,3)


@Module({
  imports: [
    ConfigModule.forRoot({
      load: [configuration],
    }),
    TypeOrmModule.forRoot({
      type: "mysql",
      host: "127.0.0.1",
      username: "root",
      password: "111111",
      database: "hc_fcg30",
      port: 3306,
      synchronize: true,
      entities: [__dirname + '/**/*.entity{.ts,.js}'],
      
      
    }),
    EmployeeModule,
    VehicleAppModule,
    KafkaModule,
  ],
  controllers: [
    CatController,
  ],
  providers: [
    AppService,
    CatService,
    EnterPersonModule,
    EnterPersonModule2,
    
  ],
})
export class AppModule implements OnModuleInit {
  async onModuleInit() {
    // console.log("aaaaaaaaa");
  }
  
}
