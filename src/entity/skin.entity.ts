import {Column, CreateDateColumn, Entity, JoinColumn, OneToOne, PrimaryGeneratedColumn} from 'typeorm';
import {UserEntity} from "./user.entity";

@Entity()
export class SkinEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({
    default: 0,
  })
  type: number; //0-steven  1-alex

  @Column({
    default: '9b155b4668427669ca9ed3828024531bc52fca1dcf8fbde8ccac3d9d9b53e3cf',
  })
  hash: string;

  @OneToOne(() => UserEntity)
  @JoinColumn()
  uploader: number;//上传者id

  @Column({
    default: ""
  })
  description: string;

  @Column({
    default: 0
  })
  like: number;//点赞数

  @CreateDateColumn()
  uploadTime: number;
}
