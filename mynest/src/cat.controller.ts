import { Controller, Get } from '@nestjs/common';
import { CatService } from './cat.service';

@Controller()
export class CatController {
  constructor(private readonly CatService: CatService) {}

  @Get("/cat")
  getHello(): string {
    return this.CatService.getHello();
  }


  @Get('/cat/:id')
  getHellow2222() : string{
    return 'bbbb'
  }
}
