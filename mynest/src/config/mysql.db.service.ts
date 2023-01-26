import { Inject, Injectable } from "@nestjs/common";
import { ConfigService } from "@nestjs/config";
import { TypeOrmModuleOptions, TypeOrmOptionsFactory } from "@nestjs/typeorm";
import { pr } from "src/app.module";
import { UserTbl } from "src/typeorm/entities/User.entite";

@Injectable()
export default class MySqlDBConfigService implements TypeOrmOptionsFactory {

  constructor(private configService: ConfigService) {}

  createTypeOrmOptions(): TypeOrmModuleOptions {
      pr(this.configService.get('host'),111)

      return {
        type: 'mysql',
        name: "mysql01",
        entities: [
          UserTbl,
          'dist/**/*.entity{.ts,.js}',
          'dist/**/object/*{.ts,.js}',
          'dist/**/model/*{.ts,.js}',
        ],
        host: this.configService.get('host'),
        port: this.configService.get<number>('port'),
        username: this.configService.get('username'),
        password: this.configService.get('password'),
        database: this.configService.get('database'),
        logging: this.configService.get('logging') === 'true',
        synchronize: this.configService.get('TYPEORM_SYNCHRONIZE') === 'true',
        migrationsRun: false,
  };
}
}