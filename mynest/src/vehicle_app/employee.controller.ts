import { Get, Controller, Param } from '@nestjs/common';
import { EmployeeService } from './employee.service';
import { Employee } from './employee.entity';

@Controller('/employee')
export class EmployeeController {
  constructor(private readonly employeeService: EmployeeService) {
      // console.log('222222222222222 EmployeeController  2222222222222222222222')

  }

  @Get()
  root(): string {
    console.log(123);
    return this.employeeService.root();
  }

  @Get('findOne/:name')
  async findOne(@Param() params): Promise<Employee> {
    console.log('222222222222222 22222222222222222  2222222222222222222222')
    console.log(params.name);
    console.log('222222222222222 22222222222222222  2222222222222222222222')
    return this.employeeService.findOne(params.name);
  }

  @Get('create')
  async create(): Promise<string> {
    console.log('1323');
    return this.employeeService.create();
  }

  @Get('create/:name')
  async create2(@Param() params): Promise<string> {
    return this.employeeService.create(params.name);
  }
}
