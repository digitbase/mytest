import { Controller, Body, Post, Get, Query } from '@nestjs/common';

import { PhotoService } from './photo.service';
import { Photo } from './photo.entity';

export class ParamsInput {
    id:string; 
    isPublic: boolean;
}

@Controller("/photo")
export class PhotoController {
  // constructor(private readonly photoService: PhotoService) {}

  @Get()
    async queryVehiclePermissionInfo(@Body() input): Promise<any> {
      console.log(input)
      // let res = await this.photoService.findAll();
    return {}
    }
    @Get("/say")
    async getInfo(@Query() input): Promise<any> {
        console.log(input)
        return {'input ':input}
    }

    @Post("/say2")
    async getInfo2(@Body() input:ParamsInput): Promise<any> {
        console.log(input)
        return {'input ':input}
    }
}
