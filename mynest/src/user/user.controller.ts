import { Controller, Get, Post,Put,Body, Delete, Param,ParseIntPipe } from '@nestjs/common';
import { pr } from 'src/app.module';
import {UserService} from "src/user/user.service"
import { UpdateUserDto, CreasteUserDto } from 'src/utils/user.dtos';
export const MUSIC_DB_CONNECTION = 'test';
export const SECRET_DB_CONNECTION = 'secret';
@Controller('user')
export class UserController {

  constructor(private userService: UserService) { }

  @Get()
  getUserInfo(@Body() input: any) {
    return this.userService.findUser();
  }

  @Put(':id')
  async updateUserById(@Param('id', ParseIntPipe) id: number, @Body() updateUserDto: UpdateUserDto) { 
    return await this.userService.updateUser(id, updateUserDto)
  }


  @Post()
  createUser(@Body() input: CreasteUserDto) {
    this.userService.createUser(input);
  }


  // @Delete()
  // // @Param("id")
  // // deleteUser()
}
