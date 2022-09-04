import { Column, Entity } from "typeorm";

@Entity("in_inspectionCheckGroup", { schema: "mybook" })
export class InInspectionCheckGroup {
  @Column("varchar", {
    primary: true,
    name: "id",
    comment: "设备组ID",
    length: 20,
  })
  id: string;

  @Column("varchar", {
    name: "masterId",
    nullable: true,
    comment: "最高级ID",
    length: 20,
  })
  masterId: string | null;

  @Column("varchar", {
    name: "parentId",
    nullable: true,
    comment: "父ID",
    length: 20,
  })
  parentId: string | null;

  @Column("tinyint", {
    name: "levelNum",
    nullable: true,
    comment: "层数",
    default: () => "'0'",
  })
  levelNum: number | null;

  @Column("varchar", { name: "groupName", comment: "设备组名", length: 64 })
  groupName: string;

  @Column("varchar", {
    name: "levelId",
    nullable: true,
    comment: "巡检等级id",
    length: 20,
  })
  levelId: string | null;

  @Column("varchar", {
    name: "typeId",
    nullable: true,
    comment: "巡检类型id",
    length: 20,
  })
  typeId: string | null;

  @Column("tinyint", { name: "groupFlg", nullable: true, comment: "是否是组" })
  groupFlg: number | null;

  @Column("varchar", {
    name: "customid",
    nullable: true,
    comment: "用户id",
    length: 20,
  })
  customid: string | null;

  @Column("varchar", {
    name: "status",
    nullable: true,
    comment: "状态",
    length: 20,
  })
  status: string | null;

  @Column("varchar", {
    name: "createdBy",
    nullable: true,
    comment: "创建人",
    length: 20,
  })
  createdBy: string | null;

  @Column("datetime", {
    name: "createdDate",
    nullable: true,
    comment: "创建时间",
  })
  createdDate: Date | null;

  @Column("varchar", {
    name: "lastModifiedBy",
    nullable: true,
    comment: "最后修改人",
    length: 20,
  })
  lastModifiedBy: string | null;

  @Column("datetime", {
    name: "lastModifiedDate",
    nullable: true,
    comment: "最后修改时间",
  })
  lastModifiedDate: Date | null;

  @Column("varchar", {
    name: "owner",
    nullable: true,
    comment: "所有人",
    length: 20,
  })
  owner: string | null;
}
