import { Module ,OnModuleInit} from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { CatController } from './cat.controller';
import { CatService } from './cat.service';
import { VehicleAppModule } from './vehicle_app/vehicle_app.module';
@Module({
  imports: [
    VehicleAppModule
  ],
  controllers: [
    CatController,
    AppController,

  ],
  providers: [
    AppService,
    CatService

  ],
})
export class AppModule implements OnModuleInit {
  async onModuleInit() {
    console.log("aaaaaaaaa");
  }
  
}
