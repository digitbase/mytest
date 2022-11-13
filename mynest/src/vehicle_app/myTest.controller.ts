import { Controller, Body, Post,Get, Query } from '@nestjs/common';



export class ParamsInput {
    id:string; 
    isPublic: boolean;
}

@Controller("/myTest")
export class MyTestController {

  constructor() {
    console.log('222222222222222  MyTestController  2222222222222222222222')

}


    @Post()
    async queryVehiclePermissionInfo(@Body() input): Promise<any> {
        console.log(input)
        return {1:1}
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
