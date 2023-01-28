import { MUSIC_DB_CONNECTION } from "src/user/user.controller";
import { Entity, Column, PrimaryGeneratedColumn } from "typeorm";

@Entity({ name: 'user_tbl' })
export class UserTbl {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({unique:true})
  user_name: string;

  @Column({})
  pwd: string;

  @Column()
  age: number;

  @Column({})
  create_date: Date;
}