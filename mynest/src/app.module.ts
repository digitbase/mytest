import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { CatController } from './cat.controller';
import { CatService } from './cat.service';

@Module({
  imports: [],
  controllers: [
    CatController,
    AppController,

  ],
  providers: [
    AppService,
    CatService

  ],
})
export class AppModule {}
