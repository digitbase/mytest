import { Inject, Module ,OnModuleInit} from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { CatController } from './cat.controller';
import { CatService } from './cat.service';
import { EnterPersonModule } from './socket01_app/enterPerson.module';
import { EnterPersonModule2 } from './socket01_app/enterPerson2.module';
import { VehicleAppModule } from './vehicle_app/vehicle_app.module';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ConfigModule, ConfigService } from '@nestjs/config';
import configuration from './config/database.config';
import {EmployeeModule} from './vehicle_app/employee.module'
import { KafkaModule } from './kafka/kafka.module';
import { DahuaConsumer } from './kafka/dahua.consumer';
import { ClientKafka, ClientProvider, ClientsModule, Transport } from '@nestjs/microservices';
import { ConsumerService } from './kafka/consumer.service';

import { ScheduleModule } from '@nestjs/schedule';
import { UserModule } from './user/user.module';
import { MUSIC_DB_CONNECTION, SECRET_DB_CONNECTION, UserController } from './user/user.controller';
import { UserService } from './user/user.service';
import { UserTbl } from './typeorm/entities/User.entite';

export function pr(input:any, type2?:number):void{
	console.log(typeof input, "==>",input);let _type = type2?type2:0;let str = " "
	if (_type > 0) {for(let i=0; i < 20; i++)  str +=_type.toString()+" ";console.log(`==============    ${str}    ===============`)}
}

const env = process.env.ENV_NODE || 'production';
console.info('---->', `.env.${env}`);


@Module({
  imports: [
    ScheduleModule.forRoot(),
    ClientsModule.register([
      {
        name: 'COMMUNICATION',
        transport: Transport.TCP,
      },
      {
        name: 'ANALYTICS',
        transport: Transport.TCP,
        options: { port: 3001 },
      },
    ]),
    ConfigModule.forRoot({
      load: [configuration],
    }),
    TypeOrmModule.forRootAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (configService: ConfigService) => ({
        type: 'mysql',
        entities: [UserTbl],
        host: configService.get('host'),
        port: configService.get<number>('port'),
        username: configService.get('username'),
        password: configService.get('password'),
        database: "hc_fcg30",
        logging: ["query"],
        synchronize: true,
      }),
      // useClass: MySqlDBConfigService,
    }),
    TypeOrmModule.forRootAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      name: 'test01',
      useFactory: (configService: ConfigService) => ({
        type: 'mysql',
        entities: [
          UserTbl,
        ],
        host: configService.get('host'),
        port: configService.get<number>('port'),
        username: configService.get('username'),
        password: configService.get('password'),
        database: "test",
        logging: ["query"],
        timezone:"local",
        synchronize: true,
      }),
      // useClass: MySqlDBConfigService,
    }),
    TypeOrmModule.forFeature( [UserTbl], 'test01' ),
    EmployeeModule,
    VehicleAppModule,
    // UserModule,
  ],
  controllers: [
    CatController,
    UserController,
  ],
  providers: [
    AppService,
    CatService,
    EnterPersonModule,
    EnterPersonModule2,
    UserService,
  ],
})
export class AppModule implements OnModuleInit {
  async onModuleInit() {
    // console.log("aaaaaaaaa");
  }
  
}
