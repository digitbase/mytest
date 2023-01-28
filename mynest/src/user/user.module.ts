import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { UserTbl } from 'src/typeorm/entities/User.entite';
import { MUSIC_DB_CONNECTION, UserController } from './user.controller';
import { UserService } from './user.service';

@Module({
  imports: [

  ],
  controllers: [UserController],
  providers: [UserService],
})
export class UserModule {}
