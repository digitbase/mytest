import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { createSecureServer } from 'http2';
import { pr } from 'src/app.module';
import { UserTbl } from 'src/typeorm/entities/User.entite';
import { Repository } from 'typeorm';

@Injectable()
export class UserService {
  constructor(
    @InjectRepository(UserTbl) private userRepository: Repository<UserTbl>,
  ) { }

  async createUser(user:any) {
    pr(user, 3333)

    const newUser = this.userRepository.create({
      ...user,
      create_date:new Date(),
    });

    pr(newUser, 333)

    return await this.userRepository.save(newUser);

  }
}
