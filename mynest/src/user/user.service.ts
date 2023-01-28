import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { createSecureServer } from 'http2';
import { format } from 'path';
import { pr } from 'src/app.module';
import { UserTbl } from 'src/typeorm/entities/User.entite';
import { CreatreUserParams,UpdateUserParams } from 'src/utils/types';
import { Repository } from 'typeorm';
import { MUSIC_DB_CONNECTION } from './user.controller';

@Injectable()
export class UserService {
  constructor(
    @InjectRepository(UserTbl,'test01' ) private userRepository: Repository<UserTbl>,
  ) { 
  }


  async updateUser(id: number, updateUserInput: UpdateUserParams) {

    pr(updateUserInput, 7766)
    return  this.userRepository.update({ id }, {
      ...updateUserInput
    })
  }

  async findUser() {
    let res = await  this.userRepository.createQueryBuilder()
      .select()
      .getMany();
    return res;
    // return await this.userRepository.find();
  }

  async createUser(user:CreatreUserParams) {
    pr(user, 3333)

    const newUser = this.userRepository.create({
      ...user,
      create_date:new Date(),
    });

    pr(newUser, 333)

    return await this.userRepository.save(newUser);

  }
}
