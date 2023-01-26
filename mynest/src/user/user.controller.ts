import { Controller, Get, Post,Body } from '@nestjs/common';
import { pr } from 'src/app.module';
import { creatreUserDTO } from 'src/utils/types';
import {UserService} from "src/user/user.service"
@Controller('user')
export class UserController {

  constructor(private userService: UserService) { }

  @Get()
  getUserInfo(@Body() input: any) {
    pr('test', 111)

    
  }

  @Post()
  createUser(@Body() input: creatreUserDTO) {
    this.userService.createUser(input);
  }

}
