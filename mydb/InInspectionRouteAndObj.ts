import { Column, Entity } from "typeorm";

@Entity("in_inspectionRouteAndObj", { schema: "mybook" })
export class InInspectionRouteAndObj {
  @Column("varchar", { primary: true, name: "id", comment: "ID", length: 20 })
  id: string;

  @Column("varchar", { name: "routeId", comment: "ID", length: 20 })
  routeId: string;

  @Column("varchar", {
    name: "objId",
    nullable: true,
    comment: "状态",
    length: 20,
  })
  objId: string | null;

  @Column("varchar", {
    name: "typeId",
    nullable: true,
    comment: "类型id",
    length: 20,
  })
  typeId: string | null;

  @Column("varchar", {
    name: "orgId",
    nullable: true,
    comment: "组id",
    length: 20,
  })
  orgId: string | null;

  @Column("varchar", {
    name: "leaderId",
    nullable: true,
    comment: "负责人id",
    length: 20,
  })
  leaderId: string | null;

  @Column("mediumtext", { name: "remark", nullable: true, comment: "备注" })
  remark: string | null;

  @Column("varchar", {
    name: "customid",
    nullable: true,
    comment: "用户id",
    length: 20,
  })
  customid: string | null;

  @Column("varchar", {
    name: "owner",
    nullable: true,
    comment: "所有人",
    length: 20,
  })
  owner: string | null;

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
    name: "installedPackage",
    nullable: true,
    comment: "已安装的软件包",
    length: 20,
  })
  installedPackage: string | null;
}
