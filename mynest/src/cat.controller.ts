import { Controller, Get } from '@nestjs/common';
import { CatService } from './cat.service';
import { EnterPersonModule } from './socket01_app/enterPerson.module';
import { EnterPersonModule2 } from './socket01_app/enterPerson2.module';

@Controller()
export class CatController {

  constructor(private readonly CatService: CatService,
    private gateWay01: EnterPersonModule,
    private gateWay02: EnterPersonModule2,
  
  ) { }

  @Get("/cat")
  async getHello() {
    let msg = {
      topic: "test",
      msg:"nihao",
    }
    let str = JSON.stringify(msg);
    let res1 = await this.gateWay01.pushMsg(str);
    let res2 = await this.gateWay02.pushMsg(str);

    return this.CatService.getHello();

  }


  @Get('/:id')
  getHellow2222() : string{
    return 'bbbb'
  }
}
