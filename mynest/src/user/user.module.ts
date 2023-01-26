import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { UserTbl } from 'src/typeorm/entities/User.entite';
import { UserController } from './user.controller';
import { UserService } from './user.service';

@Module({
  imports: [TypeOrmModule.forFeature([
    UserTbl
  ])],
  controllers: [UserController],
  providers: [UserService]
})
export class UserModule {}
