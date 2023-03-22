import {
  Column,
  CreateDateColumn,
  Entity,
  JoinColumn,
  OneToOne,
  PrimaryGeneratedColumn,
  UpdateDateColumn,
} from 'typeorm';
import {IpEntity} from './ip.entity';
import {SkinEntity} from './skin.entity';
import {TokenEntity} from './token.entity';

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

  @Column({
    default: false,
  })
  verified: boolean;

  @Column({
    default: false,
  })
  isBanned: boolean;

  @OneToOne(() => SkinEntity)
  @JoinColumn()
  skin: SkinEntity;

  @OneToOne(() => TokenEntity)
  @JoinColumn()
  token: TokenEntity;

  @OneToOne(() => IpEntity)
  @JoinColumn()
  ip: IpEntity;

  @CreateDateColumn()
  register: number;

  @UpdateDateColumn()
  lastLogged: number;
}
