import {
  Column,
  CreateDateColumn,
  Entity,
  JoinColumn,
  OneToMany,
  OneToOne,
  PrimaryGeneratedColumn,
  UpdateDateColumn,
} from 'typeorm';
import {IpEntity} from './ip.entity';
import {SkinEntity} from './skin.entity';
import {TokenEntity} from "./token.entity";

@Entity()
export class UserEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  uuid: string;

  @Column()
  playerName: string;

  @Column()
  password: string;

  @Column()
  email: string;

  @Column()
  score: number;

  @Column({
    default: 1          //0-封禁 1-游客 2-验证用户 99-超级管理员
  })
  permission: number;

  @OneToOne(() => SkinEntity)
  @JoinColumn()
  skin: SkinEntity;

  @OneToOne(() => IpEntity)
  @JoinColumn()
  ip: IpEntity;

  @OneToMany(type => TokenEntity, token => token.user)
  tokens: TokenEntity[];

  @CreateDateColumn()
  register: number;

  @UpdateDateColumn()
  lastLogged: number;
}
