import { Entity, Column, PrimaryGeneratedColumn } from "typeorm";

@Entity({ name: 'user_tbl' })
export class UserTbl {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({})
  user_name: string;

  @Column({})
  pwd: string;

  @Column({})
  age: number;

  @Column({})
  create_date: Date;
}